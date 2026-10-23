"""Intents, patterns, responses and sample hospital data."""

DEPARTMENTS = ["Cardiology", "Orthopedics", "Pediatrics", "General Medicine", "Dermatology"]

DOCTORS = [  # name, department, fee, days
    ("Dr. Anil Kumar", "Cardiology", 600, "Mon,Wed,Fri"),
    ("Dr. Suresh Pillai", "Orthopedics", 550, "Tue,Thu,Sat"),
    ("Dr. Meera Nair", "Pediatrics", 500, "Mon,Tue,Thu,Fri"),
    ("Dr. Fathima Rahman", "General Medicine", 400, "Mon,Tue,Wed,Thu,Fri,Sat"),
    ("Dr. Rohit Menon", "Dermatology", 450, "Wed,Thu,Sat"),
]

INTENTS = {
"greeting": {
  "patterns": ["hi", "hello", "hey there", "good morning", "good evening", "good afternoon",
               "hello bot", "hi there", "is anyone there", "hey", "namaste", "hello good day"],
  "responses": ["Hello! Welcome to City Hospital. How can I help you today?",
                "Hi there! I can help with appointments, timings, fees and more."]},
"goodbye": {
  "patterns": ["bye", "goodbye", "see you later", "see you", "talk to you later", "i am leaving",
               "that is all", "ok bye", "have a nice day", "catch you later"],
  "responses": ["Goodbye! Take care and stay healthy.", "Thank you for contacting City Hospital. Get well soon!"]},
"thanks": {
  "patterns": ["thanks", "thank you", "thanks a lot", "thank you so much", "that was helpful",
               "great thanks", "appreciate it", "many thanks", "thanks for the help", "awesome thank you"],
  "responses": ["You're welcome! Anything else I can help with?", "Happy to help!"]},
"timings": {
  "patterns": ["what are the hospital timings", "when does the hospital open", "opening hours",
               "what time do you close", "is the hospital open on sunday", "OPD timings",
               "working hours of hospital", "when is the outpatient department open",
               "what are your working hours", "hospital open time", "till what time is OPD open",
               "clinic timing please"],
  "responses": ["OPD timings: Mon-Sat, 9:00 AM to 5:00 PM. Emergency services are open 24x7."]},
"visiting_hours": {
  "patterns": ["what are the visiting hours", "when can I visit a patient", "visiting time for ward",
               "can I visit my relative in the hospital", "visitor timings", "when are visitors allowed",
               "ICU visiting hours", "how many visitors are allowed", "visiting time in the evening",
               "can I meet the admitted patient"],
  "responses": ["General ward visiting hours: 4:00 PM to 6:00 PM daily. ICU visits are limited to 15 minutes with staff permission."]},
"departments": {
  "patterns": ["which departments do you have", "list of departments", "what specialities are available",
               "what services do you offer", "do you have a cardiology department",
               "available departments", "what treatments are available", "show me departments",
               "which specialists are there", "tell me about your departments"],
  "responses": ["We have several departments."]},
"doctor_info": {
  "patterns": ["which doctors are available", "list of doctors", "who is the cardiologist",
               "tell me about the doctors", "is there a skin specialist", "doctor availability",
               "which doctor should I see for a child", "names of doctors", "do you have an orthopedic doctor",
               "doctor schedule", "which days is the doctor available"],
  "responses": ["Here are our doctors."]},
"fees": {
  "patterns": ["what is the consultation fee", "how much does a consultation cost", "doctor fees",
               "what is the charge for appointment", "consultation charges", "how much to see a doctor",
               "cost of visiting a specialist", "what are the fees", "price of consultation",
               "how much do I have to pay"],
  "responses": ["Consultation fees depend on the doctor."]},
"location": {
  "patterns": ["where is the hospital located", "what is your address", "how do I reach the hospital",
               "hospital location", "give me directions", "where are you situated",
               "nearest landmark to hospital", "is there parking available", "how to get to the hospital",
               "share the hospital address"],
  "responses": ["City Hospital, MG Road, Kochi, Kerala 682016. Free parking is available for patients and visitors."]},
"insurance": {
  "patterns": ["do you accept insurance", "which insurance is accepted", "is cashless treatment available",
               "medical insurance policy", "do you take health insurance", "insurance claim process",
               "can I use my mediclaim", "are government health schemes accepted",
               "cashless facility", "tpa insurance accepted"],
  "responses": ["We accept most major insurance providers and offer cashless treatment. Please bring your insurance card and ID proof to the help desk."]},
"lab_reports": {
  "patterns": ["how do I get my lab report", "when will my test results be ready", "collect blood test report",
               "where to collect reports", "online lab reports", "lab timings", "how long for report delivery",
               "can I download my report", "blood test report status", "scan report collection"],
  "responses": ["Blood test reports are ready within 24 hours; scans within 48 hours. Collect them at the lab counter (7 AM to 7 PM) with your receipt."]},
"contact": {
  "patterns": ["what is your phone number", "contact number", "how can I contact the hospital",
               "email address of hospital", "customer care number", "helpline number",
               "how to reach the reception", "give me your contact details", "call the hospital",
               "enquiry number"],
  "responses": ["Reception: 0484-1234567 | Email: info@cityhospital.example | Ambulance: 108"]},
"book_appointment": {
  "patterns": ["I want to book an appointment", "book an appointment", "I need to see a doctor",
               "schedule a consultation", "can I get an appointment", "need a slot with a doctor",
               "appointment with cardiologist", "make a booking", "I would like to consult a doctor",
               "fix an appointment for me", "book a doctor visit", "I need a doctor appointment tomorrow"],
  "responses": ["Let's book your appointment."]},
"check_appointment": {
  "patterns": ["check my appointment", "what is my appointment status", "show my booking",
               "when is my appointment", "view my appointments", "do I have an appointment",
               "confirm my appointment details", "my upcoming appointment", "appointment details please",
               "look up my booking"],
  "responses": ["Let me look that up."]},
"cancel_appointment": {
  "patterns": ["cancel my appointment", "I want to cancel my booking", "please cancel the appointment",
               "cancel appointment", "I can not come for my appointment", "remove my booking",
               "delete my appointment", "I need to cancel my visit", "call off my appointment",
               "cancel my doctor visit"],
  "responses": ["I can help you cancel."]},
"emergency": {
  "patterns": ["this is an emergency", "I have severe chest pain", "someone is unconscious",
               "need an ambulance urgently", "heart attack", "accident emergency", "he is not breathing",
               "heavy bleeding", "urgent help needed", "call ambulance", "I think I am having a stroke",
               "poisoning emergency"],
  "responses": ["Please call 112 or go to the nearest emergency department immediately."]},
}
