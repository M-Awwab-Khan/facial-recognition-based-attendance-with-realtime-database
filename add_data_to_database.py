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
    },
    "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "batch": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "batch": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "batch": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for k, v in data.items():
    ref.child(k).set(v)