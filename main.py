import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
    check, frame = video.read()
    print(frame)  # to Print All Array seen on Camera
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gua = cv2.GaussianBlur(gray_frame, (21,21), 0)




    if first_frame is None:
        first_frame = gray_frame_gua

    delta_frame = cv2.absdiff(first_frame, gray_frame_gua)
    cv2.imshow("KingVik Planet Camera", gray_frame_gua)
    #print(delta_frame) # to Print All Array seen on Camera


    threshold_frame = cv2.threshold(delta_frame, 75, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("KingVik Planet Camera", threshold_frame)



    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()