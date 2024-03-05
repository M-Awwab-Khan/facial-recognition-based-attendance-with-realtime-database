import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facial-attendance-realtime-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "280406": {
        "name": "Muhammad Awwab Khan",
        "major": "Software Engineering",
        "batch": 2023,
        "total_attendance": 3,
        "standing": "E",
        "year": 1,
        "last_attendance_time": "2024-03-05 18:05:53"
    }
}

for k, v in data.items():
    ref.child(k).set(v)