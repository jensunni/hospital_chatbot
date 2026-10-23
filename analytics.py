import os, pandas as pd, seaborn as sns, matplotlib
matplotlib.use("Agg")  
# Anti-Grain Geometry (AGG) is a high-performance, open-source 2D vector 
# graphics library written in C++ by Maxim Shemanarev.
   
import matplotlib.pyplot as plt
from db_utils import q 

os.makedirs("charts", exist_ok=True)  # Create a folder charts if not exists
sns.set_theme(style="whitegrid")      # Setting default theme

msgs = pd.DataFrame(q("SELECT * FROM messages"))
appts = pd.DataFrame(q("""SELECT a.*, d.name AS doctor, dp.name AS dept FROM appointments a
                          JOIN doctors d USING(doctor_id) JOIN departments dp USING(dept_id)"""))

def save(name): 
    plt.tight_layout()
    plt.savefig(f"charts/{name}.png", dpi=150)
    plt.close()

if not msgs.empty:
    msgs["created_at"] = pd.to_datetime(msgs["created_at"])
    plt.figure(figsize=(8, 5))
    sns.countplot(y="predicted_intent", data=msgs, order=msgs.predicted_intent.value_counts().index)
    plt.title("Most frequent intents")
    save("intent_frequency")

    plt.figure(figsize=(6, 4)); sns.histplot(msgs.confidence, bins=15)
    plt.title("Prediction confidence")
    save("confidence_distribution")

    heat = msgs.assign(day=msgs.created_at.dt.day_name(), hour=msgs.created_at.dt.hour) \
               .pivot_table(index="day", columns="hour", values="msg_id", aggfunc="count", fill_value=0)
    plt.figure(figsize=(10, 4))
    sns.heatmap(heat, cmap="YlGnBu", annot=True, fmt="d")
    plt.title("Messages by day and hour")
    save("busy_times_heatmap")

    fb = msgs.feedback.dropna()
    fallback = (msgs.predicted_intent == "fallback").mean() * 100
    print(f"Total messages: {len(msgs)} | Fallback rate: {fallback:.1f}%")
    if len(fb): print(f"Positive feedback: {fb.mean()*100:.1f}% of {len(fb)} ratings")
    print("\nUnrecognized questions (add these as new patterns):")
    print(msgs.loc[msgs.predicted_intent == "fallback", "user_text"].drop_duplicates().to_string(index=False))

if not appts.empty:
    plt.figure(figsize=(7, 4))
    sns.countplot(x="dept", hue="status", data=appts)
    plt.xticks(rotation=20)
    plt.title("Appointments by department")
    save("appointments_by_dept")
    print(f"\nCancellation rate: {(appts.status == 'cancelled').mean()*100:.1f}%")
print("Charts saved in ./charts")