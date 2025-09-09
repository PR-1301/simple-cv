# Works with files & directories
import os
# image & video processing
import cv2 as cv
# used to delay
import time
# custom send email function
from emailing import send_email
# used to find files by matching a pattern
import glob
# allows running tasks in parallel
from threading import Thread

# 0 means primary camera
video = cv.VideoCapture(0)
# delays by 1 sec
time.sleep(1)

# captures the initial frame as None
first_frame = None
# stores as 0 for no image & 1 for image
status_list = []
# for saving image files names
count = 1

def clean():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    # no object detected
    status = 0
    # video.read() returns check (True/False if frame read correctly) and frame (the image captured).
    check, frame = video.read()

    # converts the image into grayscale eay for processing
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Blurs the image to reduce size
    gray_frame_gaus = cv.GaussianBlur(gray_frame, (21, 21), 0)

    # converts the initial first frame into grayscale as reference which detects changes
    if first_frame is None:
        first_frame = gray_frame_gaus

    # calculates the absolute difference between frames
    delta_frame = cv.absdiff(first_frame, gray_frame_gaus)

    # above 60 pixels becomes white, cv,THRESH_BINARY=CONVERTS EVERYTHING INTO BLACK & WHITE, 1 RETURNS THE IMAGE
    thresh_frame = cv.threshold(delta_frame, 60, 255, cv.THRESH_BINARY)[1]
    # dilation expands the white region & makes the image solid
    dil_frame = cv.dilate(thresh_frame, None, iterations=2)
    # shows the video
    cv.imshow("My video", dil_frame)

    # finds contours(outline) of the moving region
    # cv.RETR_EXTERNAL retrieve the outermost border
    # cv.CHAIN_APPROX_SIMPLE compresses the outer points
    contours, check = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # iterates over each outline
    for contour in contours:
        # if the area of outline line is less than 5000 pixels
        if cv.contourArea(contour)<5000:
            continue
        # Draws a green rectangle around the detected moving object.
        x, y, w, h = cv.boundingRect(contour)
        # (x, y) is the top-left corner; (x+w, y+h) is the bottom-right. 3-thickness
        rectangle = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            images_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(images_with_object, ))

        email_thread.daemon = True
        clean_thread = Thread(target=clean)
        clean_thread.daemon = True

        email_thread.start()


    cv.imshow("My video", frame)
    key = cv.waitKey(1)

    if key == ord("x"):
        break

video.release()
clean_thread.start()