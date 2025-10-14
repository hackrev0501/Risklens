from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.security.auth import get_password_hash


def run():
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.email == "admin@example.com").first():
            db.add(User(email="admin@example.com", hashed_password=get_password_hash("admin"), role="admin"))
            db.commit()
            print("Seeded admin user: admin@example.com / admin")
    finally:
        db.close()


if __name__ == "__main__":
    run()
