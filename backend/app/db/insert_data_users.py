from sqlalchemy.orm import Session
from app.models.user import User
from app.core.database import SessionLocal  # Ajusta según tu estructura

# Datos a insertar (puedes agregar/quitar usuarios aquí)
USERS = [
    {
        "user_id": "ID-87654321",
        "name": "Isaac Vera",
        "image_url": "https://utec.instructure.com/images/thumbnails/2979268/EICbIWDZKj0q3mqgUmg9KTANwF3oNr5dwkDc3Ldu",
        "last_seen": "2025-06-10T09:15:33Z",
        "recognition_count": 12,
        "tags": "Student,Authorized,Computer Science",
    },
    {
        "user_id": "ID-11223344",
        "name": "David Torres",
        "image_url": "https://utec.instructure.com/files/1717177/download?download_fr...",
        "last_seen": "2025-06-15T14:22:47Z",
        "recognition_count": 5,
        "tags": "Student,Authorized,Engineering",
    },
    {
        "user_id": "ID-55667788",
        "name": "Luis Mendez",
        "image_url": "https://utec.instructure.com/images/thumbnails/933351/H3JfHZ7HFJnY619Kv65qH2j2XQ89aC0hfNrgEQ5u",
        "last_seen": "2025-06-18T20:05:11Z",
        "recognition_count": 30,
        "tags": "Student,Authorized,Mathematics",
    },
    {
        "user_id": "ID-99887766",
        "name": "Aaron Camacho",
        "image_url": "https://utec.instructure.com/images/thumbnails/611072/EgihWqRkIHUCI4sYNWFfzFXNAMTwnfPaqy5ot3NG",
        "last_seen": "2025-06-20T11:45:09Z",
        "recognition_count": 18,
        "tags": "Student,Authorized,Physics",
    },
]

def fake_dni(i): return f"{10000000 + i:08d}"

def insert_users():
    db: Session = SessionLocal()
    for i, u in enumerate(USERS):
        user = User(
            user_id=u["user_id"],
            name=u["name"],
            dni=fake_dni(i),             # fake DNI
            role="Student",              # Default role
            tags=u["tags"],              # CSV
            gender="Other",              # Default gender
            date_of_birth=None,          # Optional, set None or add date
            image_url=u["image_url"],
            recognition_count=u["recognition_count"],
            last_seen=u["last_seen"],
            last_location="Main Entrance",   # Default location
            created_at=None,
        )
        db.add(user)
    db.commit()
    db.close()
    print("Inserted demo users!")

if __name__ == "__main__":
    insert_users()
