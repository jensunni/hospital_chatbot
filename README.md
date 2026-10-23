# Hospital Appointment + FAQ Chatbot (Python, NLTK, scikit-learn, MySQL, Streamlit)

## Setup
1. Install MySQL and create a user. Then set your credentials (or edit `config.py`):
   `export DB_PASSWORD=yourpassword`  (Windows: `set DB_PASSWORD=yourpassword`)
2. `pip install -r requirements.txt`
3. `python setup_db.py`   # creates tables + loads intents, patterns, doctors
4. `python train.py`      # compares 4 models, saves model.joblib + confusion_matrix.png
5. `python bot.py`        # optional: test in the terminal
6. `streamlit run app.py` # web chat UI
7. `python analytics.py`  # Seaborn charts from the logs, saved in ./charts

## Adding new intents
Insert into `intents`, `patterns`, `responses` (or edit `seed_data.py`), then re-run `python train.py`.

## Notes
- Double bookings are blocked by a MySQL unique key on (doctor, date, active slot). Cancelled slots become free again.
- Emergency keywords bypass the model. The bot never gives medical advice.
- Patient data is personal data: don't deploy publicly without authentication, HTTPS and access controls.