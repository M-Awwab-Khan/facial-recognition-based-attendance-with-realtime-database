import cv2
import pickle
import face_recognition
import os

#importing students images
folder_path = 'Images'
img_names = os.listdir(folder_path)
std_images = []
std_ids = []

for path in img_names:
    std_images.append(cv2.imread(os.path.join(folder_path, path)))
    std_ids.append(os.path.splitext(path)[0])

print(std_ids)