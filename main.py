import cv2

cap = cv2.VideoCapture(0)

img_bg = cv2.imread('Resources/background.png')

while True:
    success, img = cap.read()
    img = cv2.resize(img, (640, 480)) 

    img_bg[162:162+480, 55:55 + 640] = img

    # cv2.imshow("Webcam", img)
    cv2.imshow('Facial Attendance', img_bg)
    cv2.waitKey(1)