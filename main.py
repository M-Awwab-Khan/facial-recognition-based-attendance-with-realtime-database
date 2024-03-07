import cv2
import os
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import  storage, db

cap = cv2.VideoCapture(0)

img_bg = cv2.imread('Resources/background.png')

#importing modes images
folder_path = 'Resources/Modes'
img_names = os.listdir(folder_path)
mode_images = []

encodings_with_ids = pickle.load(open('EncodeFile.p', 'rb'))
encoding_list, std_ids = encodings_with_ids

for path in img_names:
    mode_images.append(cv2.imread(os.path.join(folder_path, path)))

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facial-attendance-realtime-default-rtdb.firebaseio.com/",
    "storageBucket": "facial-attendance-realtime.appspot.com"

})

bucket = storage.bucket()

mode = 0
counter = 0
id = -1

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 480)) 
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_current_frame = face_recognition.face_locations(imgS)
    current_face_encoding = face_recognition.face_encodings(imgS, face_current_frame)

    img_bg[162:162+480, 55:55 + 640] = img
    img_bg[44:44 + 633, 808:808 + 414] = mode_images[mode]

    for current_encoding, current_face in zip(current_face_encoding, face_current_frame):
        matches = face_recognition.compare_faces(encoding_list, current_encoding)
        face_distance = face_recognition.face_distance(encoding_list, current_encoding)
        
        match_index = np.argmin(face_distance)
        if matches[match_index]:
            y1, x2, y2, x1 = current_face
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            img_bg = cvzone.cornerRect(img_bg, bbox, rt=0)
            id = std_ids[match_index]

            if counter == 0:
                counter = 1
                mode = 1

    if counter == 1:
        print('inside test block')
        student_info = db.reference(f'Students/{id}').get()
        # Get the Image from the storage
        blob = bucket.get_blob(f'Images/{id}.png')
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        img_std = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
        ref = db.reference(f'Students/{id}')
        student_info['total_attendance'] += 1
        ref.child('total_attendance').set(student_info['total_attendance'])

    if counter <= 10 and counter != 0:
        counter += 1
        cv2.putText(img_bg, str(student_info['total_attendance']), (861, 125), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
        cv2.putText(img_bg, str(student_info['major']), (1006, 550),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img_bg, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img_bg, str(student_info['standing']), (910, 625),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(img_bg, str(student_info['year']), (1025, 625),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
        cv2.putText(img_bg, str(student_info['batch']), (1125, 625),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (100, 100, 100), 1)
        (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_DUPLEX, 1, 1)
        offset = (414 - w) // 2
        cv2.putText(img_bg, str(student_info['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (50, 50, 50), 1)
        img_bg[175:175 + 216, 909:909 + 216] = img_std

    if counter > 10 and counter <= 20:
        counter += 1
        mode = 2

    if counter >= 20:
        counter = 0
        mode = 0
        student_info = []
        img_std = []
        



    # cv2.imshow("Webcam", img)
    cv2.imshow('Facial Attendance', img_bg)
    cv2.waitKey(1)