import cv2
import imutils
import numpy as np

# set up face detection
detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
im_file = 'test.jpg'

im = cv2.imread(im_file)

# resize the frame, convert it to grayscale, and detect faces in the
# frame
frame = imutils.resize(im, width=400)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faceRects = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
	minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
rect = faceRects[0]

if len(faceRects) > 1:
    # take largest face if detected multiple
    sizes = [w * h for x, y, w, h in faceRects]
    bestIdx = np.argmax(sizes)
    rect = faceRects[bestIdx]

# loop over the faces and draw a rectangle around each
x, y, w, h = rect
cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Frame", frame)
key = cv2.waitKey(0)
