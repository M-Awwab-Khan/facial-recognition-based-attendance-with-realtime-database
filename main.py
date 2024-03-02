import cv2
import os

cap = cv2.VideoCapture(0)

img_bg = cv2.imread('Resources/background.png')

#importing modes images
folder_path = 'Resources/Modes'
img_names = os.listdir(folder_path)
mode_images = []

for path in img_names:
    mode_images.append(cv2.imread(os.path.join(folder_path, path)))

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 480)) 

    img_bg[162:162+480, 55:55 + 640] = img
    img_bg[44:44 + 633, 808:808 + 414] = mode_images[1]

    # cv2.imshow("Webcam", img)
    cv2.imshow('Facial Attendance', img_bg)
    cv2.waitKey(1)