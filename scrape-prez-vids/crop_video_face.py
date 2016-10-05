import cv2
import os
import glob
import imutils
import numpy as np

showVid = False # whether to display video--currently not working in ipython

# set up face detection
detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# incase you run this in ipython...
#cv2.startWindowThread()

testFile = glob.iglob('videos/' + '*.[mM][pP]4').next()
vid = cv2.VideoCapture(testFile)

# jump past the intro
# http://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
start_at = 0 # start the video at (milliseconds), for skipping intros
vid.set(0, start_at)

face_rect_list = []
face_rect_times = []
video_times = [] # for keeping track of the whole video
# so we can get fraction with faces

while True:
    # check out one frame
    (grabbed, frame) = vid.read()
    if frame is None:
        break

    # resize the frame, convert it to grayscale, and detect faces in the
    # frame
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
    	minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

    if len(faceRects) < 1:
        continue

    rect = faceRects[0]

    if len(faceRects) > 1:
        # take largest face if detected multiple
        sizes = [w * h for x, y, w, h in faceRects]
        bestIdx = np.argmax(sizes)
        rect = faceRects[bestIdx]

    # store rectangle positions and times
    face_rect_list.append(rect)
    face_rect_times.append(vid.get(0))

    x, y, w, h = rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if showVid:
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
