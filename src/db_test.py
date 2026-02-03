from sqlalchemy import text
from database import engine


def test_db_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("DB connection successful:", result.scalar())


if __name__ == "__main__":
    test_db_connection()
