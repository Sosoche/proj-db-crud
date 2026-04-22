import time
from app import create_app
from app.models import db


def init_db() -> None:
    """
    Инициализирует БД с проверкой готовности сервера.
    """
    app = create_app()
    with app.app_context():
        retries = 5
        while retries > 0:
            try:
                db.create_all()
                print("Database initialized.")
                break
            except Exception as e:
                retries -= 1
                print(f"Waiting for database... ({retries} retries left)")
                time.sleep(5)
        else:
            print("Could not connect to database.")


if __name__ == "__main__":
    init_db()
