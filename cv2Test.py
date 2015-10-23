import cv2
import numpy as np

# Import local libardrone from python-ardrone git clone
import sys
sys.path.append('./python-ardrone/')
import libardrone
def main():
    # Get Video Stream from Quadcopter
    vid = cv2.VideoCapture('tcp://192.168.1.1:5555')

    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    # Is the Video Still active
    running = True

    while running:
         # Get current frame of Video Stream
         running, frame = vid.read()
         if running:

             # Create grayscale version of video feed for OpenCV
             grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

             # Detect faces in current frame
             #detectFaces(faceCascade, grayscale, frame)
             cv2.imshow('frame', frame)
             if cv2.waitKey(1) & 0xFF == 27:
                 # Escape Key pressed
                 running = false
    vid.release()
    cv2.destroyAllWindows()

def detectFaces(faceCascade, grayscale, frame):
    # Create array of faces found using Haar Cascade face detection algorithm
    faces = faceCascade.detectMultiScale(grayscale, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

if __name__ == '__main__':
    main()
