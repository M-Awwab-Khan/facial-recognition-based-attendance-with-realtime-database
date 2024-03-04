import cv2
import os
import pickle
import numpy as np
import face_recognition

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

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 480)) 
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_current_frame = face_recognition.face_locations(imgS)
    current_face_encoding = face_recognition.face_encodings(imgS, face_current_frame)

    img_bg[162:162+480, 55:55 + 640] = img
    img_bg[44:44 + 633, 808:808 + 414] = mode_images[1]

    for current_encoding, current_face in zip(current_face_encoding, face_current_frame):
        matches = face_recognition.compare_faces(encoding_list, current_encoding)
        face_distance = face_recognition.face_distance(encoding_list, current_encoding)
        
        match_index = np.argmin(face_distance)
        if matches[match_index]:
            print('Known face detected', std_ids[match_index])

    # cv2.imshow("Webcam", img)
    cv2.imshow('Facial Attendance', img_bg)
    cv2.waitKey(1)