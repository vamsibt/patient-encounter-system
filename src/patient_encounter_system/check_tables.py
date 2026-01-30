from sqlalchemy import inspect
from patient_encounter_system.database import engine

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in DB:", tables)

if __name__ == "__main__":
    check_tables()
