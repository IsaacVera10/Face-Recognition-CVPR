from app.models.logs import RecognitionLog
from app.core.database import SessionLocal
from datetime import datetime
from app.models.user import User

RECOGNITION_LOGS = [
    {
        "user_id": "ID-87654321",
        "timestamp": "2025-06-04T04:58:20",
        "location": "Main Entrance",
        "confidence": 0.95,
    },
    {
        "user_id": "ID-87654321",
        "timestamp": "2025-06-04T03:15:33",
        "location": "Parking Lot A",
        "confidence": 0.98,
    },
    {
        "user_id": "ID-11223344",
        "timestamp": "2025-06-03T12:45:20",
        "location": "Main Exit",
        "confidence": 0.94,
    },
    {
        "user_id": "ID-55667788",
        "timestamp": "2025-06-03T04:12:45",
        "location": "Main Entrance",
        "confidence": 0.97,
    },
    {
        "user_id": "ID-99887766",
        "timestamp": "2025-06-02T12:30:10",
        "location": "Main Exit",
        "confidence": 0.93,
    },
    {
        "user_id": "ID-11223344",
        "timestamp": "2025-06-01T08:15:00",
        "location": "Main Entrance",
        "confidence": 0.92,
    },
    {
        "user_id": "ID-99887766",
        "timestamp": "2025-06-01T10:10:10",
        "location": "Parking Lot B",
        "confidence": 0.96,
    },
    {
        "user_id": "ID-55667788",
        "timestamp": "2025-06-01T14:25:40",
        "location": "Main Exit",
        "confidence": 0.91,
    },
]
def insert_recognition_logs():
    db = SessionLocal()
    for log in RECOGNITION_LOGS:
        db_log = RecognitionLog(
            user_id=log["user_id"],
            timestamp=datetime.fromisoformat(log["timestamp"]),
            location=log["location"],
            confidence=log["confidence"]
        )
        db.add(db_log)
    db.commit()
    db.close()
    print("Inserted recognition logs!")

if __name__ == "__main__":
    insert_recognition_logs()
