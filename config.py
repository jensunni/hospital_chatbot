import os

DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
    database=os.getenv("DB_NAME", "hospital_bot"),
)
MODEL_PATH = "model.joblib"
CONFIDENCE_THRESHOLD = 0.40
SLOTS = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]