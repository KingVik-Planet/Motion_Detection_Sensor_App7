import cv2
import time
from emailing import send_email
import glob
import os
from threading import Thread
from datetime import datetime

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

#Sensitivity Threshold for motion Detection
SENSITIVITY_THRESHOLD = 500

def clean_folder():
    print("Clean_function has started")
    images = glob.glob("images/*.png")
    for image in images:
        os.unlink(image)
    print("clean_function ended")


# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
while True:
    status = 0
    check, frame = video.read()

    #Flip the Frame Horizontally
    frame = cv2.flip(frame, 1)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
        continue

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 75, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My camera", dil_frame)


    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    #Cirecle Frame
    # for contour in contours:
    #     if cv2.contourArea(contour) < SENSITIVITY_THRESHOLD:
    #         continue
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.circle(frame, (x + w // 2, y + h // 2), min(w, h) // 2, (255, 0, 0), 3)
    #
    # contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, w, y, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

#Face Detection on Rectangle
        # faces = face_cascade.detectMultiScale(gray_frame_gau,  scaleFactor=1.1, minNeighbors=5)
        # for (fx, fy, fw, fh) in faces:
        #     cv2.rectangle(frame, (fx, fy), (fx + fw, fy +fh), (0, 255, 0), 2)
#Face Detection on circle
        faces = face_cascade.detectMultiScale(gray_frame_gau, scaleFactor=1.1, minNeighbors=5)
        for (fx, fy, fw, fh) in faces:
            center_x = fx + fw // 2
            center_y = fy + fh // 2
            radius = max(fw, fh) // 2
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)

        status = 1
        #Adding Time Stamp
        timestamp = datetime.now().strftime("Cam1: Date:%d/%m/%Y:Time:%H:%M:%S")
        cv2.putText(frame, timestamp, (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)
        cv2.imwrite(f"images/{count}.png", frame)
        count = count + 1
        all_images = glob.glob("*images/*.png")
        index = int(len(all_images)/2)
        image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()
        clean_thread.start()

    print(status_list)

    cv2.imshow("Detection Screen", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
