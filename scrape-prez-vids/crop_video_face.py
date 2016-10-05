import cv2
import os
import glob
import imutils
import numpy as np
import argparse
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser(description='Process obama weekly addresses.')

ap.add_argument("-sv", "--showvid", help="Display the video while processing.", default=False)

args = vars(ap.parse_args())

showVid = args["showvid"] # whether to display video--currently not working in ipython

# set up face detection
detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')

# incase you run this in ipython...
#cv2.startWindowThread()

# this is a nice way to grab the first file from the folder
# testFile = glob.iglob('videos/' + '*.[mM][pP]4').next() # was 'videos/20161001_Weekly_Address_HD.mp4'
testFile = 'videos/20161001_Weekly_Address_HD.mp4'

vid = cv2.VideoCapture(testFile)

# jump past the intro
# http://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# http://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get
start_at = 0 # start the video at (milliseconds), for skipping intros
if start_at != 0:
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

    video_times.append(vid.get(0))

    # resize the frame, convert it to grayscale, and detect faces in the
    # frame
    frame = imutils.resize(frame, width=400)
    video_full_size = frame.shape[:2]
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

EDA = False
if EDA == True: # exploratory data analysis
    # convert face_rect_list to a np array so we can manipulate it easier
    face_rect_list = np.array(face_rect_list)
    face_rect_sizes = face_rect_list[:, 2] * face_rect_list[:, 3]

    # some exploratory analysis of the distribution of face rectangle sizes
    plt.hist(face_rect_sizes, bins=30)
    plt.show()
    # we can see it's bimodal for the test video

    plt.plot(face_rect_times, face_rect_sizes)
    plt.show()
    # they must've zoomed in about 1/3 through the video, because the face size
    # goes up

    # look at pct of frame taken up by face
    plt.plot(face_rect_times, face_rect_sizes / float(video_full_size[0] * video_full_size[1]) * 100)
    plt.ylabel('face area as % of frame')
    plt.xlabel('time (ms)')
    plt.show()
