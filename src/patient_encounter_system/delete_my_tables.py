from sqlalchemy import text
from patient_encounter_system.database import engine

TABLES = [
    "vamsi_appointments",
    "vamsi_patients",
    "vamsi_doctors",
]


def delete_all_tables():
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        for table in TABLES:
            print(f"🧨 Dropping table: {table}")
            conn.execute(text(f"DROP TABLE IF EXISTS {table};"))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        conn.commit()

    print("✅ All tables deleted successfully")


if __name__ == "__main__":
    delete_all_tables()
