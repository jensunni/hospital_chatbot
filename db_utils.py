import mysql.connector
from config import DB

_conn = None

def conn():
    global _conn
    if _conn is None or not _conn.is_connected():
        _conn = mysql.connector.connect(**DB)
    return _conn

def q(sql, params=(), write=False):
    """Run a query. SELECT -> list of dicts; write -> lastrowid."""
    c = conn().cursor(dictionary=True)  
    # returns results as a dictionaries instead of list of tuples
    try:
        c.execute(sql, params)
        if write:
            conn().commit()
            return c.lastrowid 
            # return the autoincremented id of every row inserted
        return c.fetchall()
    finally:
        c.close()