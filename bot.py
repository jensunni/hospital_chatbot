import re, random, datetime as dt
import dateparser, joblib, mysql.connector
# **joblib** designed to provide lightweight pipelining and efficient processing, 
# particularly for objects containing large NumPy arrays
# **dateparser** is a popular Python library designed to parse human-readable, 
# natural language dates and times into standard Python datetime objects.

from db_utils import q
from nlp_utils import preprocess
from config import MODEL_PATH, CONFIDENCE_THRESHOLD, SLOTS

model = joblib.load(MODEL_PATH)

EMERGENCY_WORDS = re.compile(
    r"\b(emergency|ambulance|unconscious|not breathing|heart attack|stroke|chest pain|"
    r"heavy bleeding|poison|overdose|suicide)\b", re.I)
EMERGENCY_REPLY = ("🚨 This sounds urgent. Please call **112** (ambulance: 108) or go to the nearest "
                   "emergency department right away. Do not wait for an appointment.")

# ------------------------------------------------------------ helpers
def predict(text):
    p = model.predict_proba([preprocess(text)])[0] 
    # extract 0th index of array of probability estimates for all possible classes
    return model.classes_[p.argmax()], float(p.max())
    # returns tuple of actual label['positive','negative','neutral'] of max probability 
    # and its value of your model that was trained

def dept_names():
    return [r["name"] for r in q("SELECT name FROM departments")]

def find_department(text):
    t = text.lower()
    for d in q("SELECT * FROM departments"):
        if d["name"].lower() in t or d["name"].lower()[:5] in t:   # 'cardio' matches 'cardiologist'
            return d

def parse_date(text):
    d = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    # settings inform that it is future day 
    return d.date() if d and d.date() >= dt.date.today() else None
    # extract date only and check it is today or future date, if not return None

def parse_phone(text):
    m = re.search(r"(?<!\d)\d{10}(?!\d)", text)
    # First it searches the mobile number
    return m.group() if m else None
    # Matches the mobile number already searched if not found then none

def parse_time(text):
    m = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", text.lower())
    # First it searches the time in 12 hour format
    if not m: 
        return None
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    # Matches the time in hour,minutes and AM/PM
    if (ap == "pm" and h < 12): 
        h += 12
    if (ap is None and 1 <= h <= 8): # Time to 24-hour format
        h += 12          
    return f"{h:02d}:{mi:02d}" if h < 24 and mi < 60 else None

def free_slots(doctor_id, date):
    rows = q("SELECT appt_time FROM appointments WHERE doctor_id=%s AND appt_date=%s AND status='booked'",
    (doctor_id, date))
    taken = {str(r["appt_time"])[:5].zfill(5) for r in rows}
    # loop through database rows and read appointment time and store in set of taken slots 
    # zfill(5) ensures that the time string is always 5 characters long, 
    # padding with leading zeros if necessary (e.g., "9:00" becomes "09:00").
    if date == dt.date.today():
        now = dt.datetime.now().strftime("%H:%M")
        taken |= {s for s in SLOTS if s <= now} 
    # (|=) is a set union operator 
    # takes all appointment slots that are already taken and 
    # have passed for today are added to the taken set
    return [s for s in SLOTS if s not in taken]
def doctor_list_text():
    rows = q("""SELECT d.name, d.consult_fee, d.available_days, dp.name AS dept
                FROM doctors d JOIN departments dp USING(dept_id)""")
    return "\n".join(f"- {r['name']} ({r['dept']}) – ₹{r['consult_fee']:.0f} – {r['available_days']}"
                     for r in rows)

# ------------------------------------------------------------ booking flow
def booking_step(text, s):
    d, step = s["data"], s["step"]

    if step == "dept":
        dept = find_department(text)
        if not dept:
            return "Please choose a department: " + ", ".join(dept_names())
        d["dept"] = dept
        d["doctors"] = q("SELECT * FROM doctors WHERE dept_id=%s", (dept["dept_id"],))
        s["step"] = "doctor"
        return "Available doctors:\n" + "\n".join(
            f"- {x['name']} (₹{x['consult_fee']:.0f}, {x['available_days']})" for x in d["doctors"]) \
            + "\n\nWhich doctor would you like?"

    if step == "doctor":
        doc = next((x for x in d["doctors"] if x["name"].lower().split()[-1] in text.lower()), None)
        if not doc and len(d["doctors"]) == 1 and text.lower().startswith(("y", "ok")):
            doc = d["doctors"][0]
        if not doc: 
            return "Please type the doctor's name from the list."
        d["doctor"] = doc
        s["step"] = "date"
        return "Which date? (e.g.  5 Oct , 6 Nov )" 

    if step == "date":
        date = parse_date(text)
        if not date: 
            return "I couldn't understand that date. Try '12 Oct'."
        if date.strftime("%a") not in d["doctor"]["available_days"]:
            return f"{d['doctor']['name']} is available on {d['doctor']['available_days']}. Pick another date."
        slots = free_slots(d["doctor"]["doctor_id"], date)
        if not slots: 
            return "No free slots that day. Please try another date."
        d["date"] = date
        s["step"] = "time"
        return "Free slots: " + ", ".join(slots) + "\nWhich time?"

    if step == "time":
        t = parse_time(text)
        if t not in free_slots(d["doctor"]["doctor_id"], d["date"]):
            return "Please pick one of the free slots listed (e.g. 10:00 or 3 pm)."
        d["time"] = t
        s["step"] = "name"
        return "Patient's full name?"

    if step == "name":
        if len(text.strip()) < 2: 
            return "Please enter the patient's name."
        d["name"] = text.strip().title()
        s["step"] = "phone"
        return "Mobile number (10 digits)?"

    if step == "phone":
        ph = parse_phone(text)
        if not ph: 
            return "Please enter a valid 10-digit number."
        d["phone"] = ph
        s["step"] = "confirm"
        return (f"Please confirm: **{d['doctor']['name']}** on **{d['date']}** at **{d['time']}** "
                f"for **{d['name']}** ({ph}). Shall I book it? (yes/no)")

    if step == "confirm":
        if text.lower().strip().startswith(("y", "ok", "confirm")):
            q("INSERT INTO patients(name,phone) VALUES(%s,%s) ON DUPLICATE KEY UPDATE name=VALUES(name)",
              (d["name"], d["phone"]), write=True)
            pid = q("SELECT patient_id FROM patients WHERE phone=%s", (d["phone"],))[0]["patient_id"]
            try:
                aid = q("INSERT INTO appointments(patient_id,doctor_id,appt_date,appt_time) VALUES(%s,%s,%s,%s)",
                        (pid, d["doctor"]["doctor_id"], d["date"], d["time"]), write=True)
            except mysql.connector.IntegrityError:
                s["step"] = "time"
                return "Sorry, that slot was just taken. Please choose another time."
            s.update(flow=None, step=None, data={})
            return f"✅ Booked! Your appointment ID is **#{aid}**. Please arrive 15 minutes early."
        s.update(flow=None, step=None, data={})
        return "Okay, booking cancelled."

# ------------------------------------------------------------ cancel flow
def cancel_step(text, s):
    d = s["data"]
    ph = parse_phone(text)
    if ph: 
        d["phone"] = ph
    rest = re.sub(r"\d{10}", "", text)
    m = re.search(r"\b(\d{1,7})\b", rest)
    if m: 
        d["appt_id"] = int(m.group(1))
    if "phone" not in d: return "Please share the 10-digit mobile number used for booking."
    if "appt_id" not in d: return "Please share your appointment ID (e.g. 12)."
    rows = q("""SELECT a.appt_id FROM appointments a JOIN patients p USING(patient_id)
                WHERE a.appt_id=%s AND p.phone=%s AND a.status='booked'""", (d["appt_id"], d["phone"]))
    s.update(flow=None, step=None, data={})
    if not rows: return "I couldn't find an active booking matching those details."
    q("UPDATE appointments SET status='cancelled' WHERE appt_id=%s", (rows[0]["appt_id"],), write=True)
    return f"Appointment #{rows[0]['appt_id']} has been cancelled. You can book a new one anytime."

# ------------------------------------------------------------ main entry
def handle(text, s):
    """Returns (reply, intent_tag, confidence). `s` is the session dict."""
    if EMERGENCY_WORDS.search(text):
        s.update(flow=None, step=None, data={})
        return EMERGENCY_REPLY, "emergency", 1.0

    if s.get("flow"):
        if text.lower().strip() in ("cancel", "stop", "exit", "quit", "never mind"):
            s.update(flow=None, step=None, data={})
            return "Okay, I've stopped that. How else can I help?", "flow_abort", 1.0
        flow_name = s["flow"]
        fn = booking_step if s["flow"] == "booking" else cancel_step
        reply = fn(text, s)
        return reply, flow_name + "_flow", 1.0

    tag, conf = predict(text)
    if tag == "emergency":
        return EMERGENCY_REPLY, tag, conf
    if conf < CONFIDENCE_THRESHOLD:
        return ("Sorry, I didn't understand. I can help with appointments, timings, fees, "
                "departments and doctors."), "fallback", conf

    if tag == "book_appointment":
        s.update(flow="booking", step="dept", data={})
        return "Sure! Which department? " + ", ".join(dept_names()), tag, conf

    if tag == "cancel_appointment":
        s.update(flow="cancel", step="ask", data={})
        return cancel_step(text, s) if (parse_phone(text)) else \
            "Sure. Please share your 10-digit mobile number and appointment ID.", tag, conf

    if tag == "check_appointment":
        ph = parse_phone(text)
        if not ph:
            return "Please include your 10-digit registered mobile number, e.g. 'check appointment 9876543210'.", tag, conf
        rows = q("""SELECT a.appt_id,a.appt_date,a.appt_time,d.name FROM appointments a
                    JOIN patients p USING(patient_id) JOIN doctors d USING(doctor_id)
                    WHERE p.phone=%s AND a.status='booked' AND a.appt_date>=CURDATE()
                    ORDER BY a.appt_date""", (ph,))
        reply = "\n".join(f"#{r['appt_id']}: {r['name']} on {r['appt_date']} at {str(r['appt_time'])[:5]}"
                          for r in rows) or "No upcoming appointments found for this number."
        return reply, tag, conf

    if tag == "departments":
        return "Our departments: " + ", ".join(dept_names()), tag, conf
    if tag in ("doctor_info", "fees"):
        return "Doctors, consultation fees and available days:\n" + doctor_list_text(), tag, conf

    rows = q("SELECT response FROM responses r JOIN intents i USING(intent_id) WHERE i.tag=%s", (tag,))
    return random.choice(rows)["response"], tag, conf

# ------------------------------------------------------------ logging
def log(sid, text, reply, tag="", conf=0.0):
    return q("INSERT INTO messages(session_id,user_text,predicted_intent,confidence,bot_reply) "
             "VALUES(%s,%s,%s,%s,%s)", (sid, text, tag, conf, reply), write=True)

def set_feedback(msg_id, value):
    q("UPDATE messages SET feedback=%s WHERE msg_id=%s", (value, msg_id), write=True)

# ------------------------------------------------------------ CLI test mode
if __name__ == "__main__":
    session, sid = {"flow": None}, "cli"
    print("Bot: Hello! Type 'quit' to exit.")
    while (u := input("You: ")).lower() != "quit":
        r, t, c = handle(u, session)
        log(sid, u, r, t, c)
        print(f"Bot: {r}   [{t}, {c:.2f}]")