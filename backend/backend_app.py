from fastapi import FastAPI
import sqlite3
from pathlib import Path
import models

app = FastAPI()

def get_db_connection():
    script_dir = Path(__file__).parent
    db_path = script_dir.parent / "database" / "database.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/auto/get")
async def get_autok():
    conn = get_db_connection()
    cur = conn.cursor()
    res = cur.execute("SELECT * FROM auto LIMIT 15")
    autok = res.fetchall()
    return {"auto": [dict(auto) for auto in autok]}

@app.post("/auto/add")
async def add_auto(auto: models.Auto):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO auto (gyarto, modell, ajtok_szama, uzemanyag, hengerurtartalom)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            auto.gyarto,
            auto.modell,
            auto.ajtok_szama,
            auto.uzemanyag,
            auto.hengerurtartalom
        )
    )
    conn.commit()
    return {"status": "ok"}

@app.delete("/auto/delete/{auto_id}")
async def delete_auto(auto_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM auto WHERE id = ?", (auto_id,))
    conn.commit()
    return {"status": "deleted"}
