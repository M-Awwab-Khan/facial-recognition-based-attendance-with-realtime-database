import cv2
import pickle
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import  storage

#importing students images
folder_path = 'Images'
img_names = os.listdir(folder_path)
std_images = []
std_ids = []

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facial-attendance-realtime-default-rtdb.firebaseio.com/",
    "storageBucket": "facial-attendance-realtime.appspot.com"

})


for path in img_names:
    std_images.append(cv2.imread(os.path.join(folder_path, path)))
    std_ids.append(os.path.splitext(path)[0])

    fileName = f'{folder_path}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def generate_encoding(std_images):
    encodings = []
    for img in std_images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(img)[0]
        encodings.append(encoding)

    return encodings

print("Encoding Started ...")
encoding_list = generate_encoding(std_images)
encoding_list_with_ids = [encoding_list, std_ids]
print(encoding_list)
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encoding_list_with_ids, file)
file.close()
print("File Saved")