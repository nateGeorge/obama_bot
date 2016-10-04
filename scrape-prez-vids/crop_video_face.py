import cv2
import os
import glob
import imutils


# set up face detection
detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# incase you run this in ipython...
#cv2.startWindowThread()

testFile = glob.iglob('videos/' + '*.[mM][pP]4').next()
vid = cv2.VideoCapture(testFile)

# jump past the intro
# http://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
#The first argument of cap.set(), number 2 defines that parameter for setting the frame selection.
#Number 2 defines flag CV_CAP_PROP_POS_FRAMES which is a 0-based index of the frame to be decoded/captured next.
#The second argument defines the frame number in range 0.0-1.0
frame_no = 6000
vid.set(0, frame_no)

face_rect_list = []

while True:
    # check out one frame
    (grabbed, frame) = vid.read()

    # resize the frame, convert it to grayscale, and detect faces in the
    # frame
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
    	minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

    # loop over the faces and draw a rectangle around each
    for (x, y, w, h) in faceRects:
    	cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
