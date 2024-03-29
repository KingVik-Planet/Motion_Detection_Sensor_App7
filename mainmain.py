import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gua = cv2.GaussianBlur(gray_frame, (21,21), 0)
    cv2.imshow("KingVik Planet Camera", gray_frame_gua)

    print(frame) # to Print All Array seen on Camera

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()