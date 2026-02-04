from sqlalchemy import text

from src.database import engine

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS vamsi_appointments"))
    conn.execute(text("DROP TABLE IF EXISTS vamsi_patients"))
    conn.execute(text("DROP TABLE IF EXISTS vamsi_doctors"))

print("All tables dropped successfully.")
