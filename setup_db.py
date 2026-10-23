"""Creates tables and loads seed data.  Run once:  python setup_db.py"""
import mysql.connector
from config import DB
import seed_data as sd

cfg = {k: v for k, v in DB.items() if k != "database"}
con = mysql.connector.connect(**cfg)
cur = con.cursor()

script = "\n".join(l for l in open("db/hospitalbot.sql").read().splitlines() if not l.strip().startswith("--"))
for stmt in filter(None, (s.strip() for s in script.split(";"))):
    cur.execute(stmt)
cur.execute(f"USE {DB['database']}")

# reset chatbot-brain + reference tables so the script can be re-run
cur.execute("SET FOREIGN_KEY_CHECKS=0")
for t in ("patterns", "responses", "intents", "doctors", "departments"):
    cur.execute(f"TRUNCATE TABLE {t}")
cur.execute("SET FOREIGN_KEY_CHECKS=1")

for tag, d in sd.INTENTS.items():
    cur.execute("INSERT INTO intents(tag) VALUES(%s)", (tag,))
    iid = cur.lastrowid
    cur.executemany("INSERT INTO patterns(intent_id,pattern) VALUES(%s,%s)", [(iid, p) for p in d["patterns"]])
    cur.executemany("INSERT INTO responses(intent_id,response) VALUES(%s,%s)", [(iid, r) for r in d["responses"]])

ids = {}
for name in sd.DEPARTMENTS:
    cur.execute("INSERT INTO departments(name) VALUES(%s)", (name,))
    ids[name] = cur.lastrowid
for name, dept, fee, days in sd.DOCTORS:
    cur.execute("INSERT INTO doctors(name,dept_id,consult_fee,available_days) VALUES(%s,%s,%s,%s)",
                (name, ids[dept], fee, days))
con.commit()
print("Database ready:", len(sd.INTENTS), "intents,", len(sd.DOCTORS), "doctors.")
