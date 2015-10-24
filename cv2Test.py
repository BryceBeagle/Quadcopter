import cv2
from threading import Thread

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone


def main():
    global frame
    global frameMod

    # Is the video still active
    global running
    running = True

    # Initialize frame and frameMod to None to help mitigate race conditions
    frame, frameMod = None

    robotThread = Thread(target = detectFaces)
    robotThread.start()

    # Get Video Stream from Quadcopter
    vid = cv2.VideoCapture('tcp://192.168.1.1:5555')

    while running:
        # Get current frame of Video Stream
        running, frame = vid.read()

        if running:

            # Check if frameMod has been initialized
            if len(frameMod):

                # Draw current frame to OpenCV window
                cv2.imshow('frame', frameMod)

            # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
            if cv2.waitKey(1) & 0xFF == 27:
                running = False

    vid.release()
    cv2.destroyAllWindows()

    robotThread.join(1000)


def detectFaces():
    """Detect faces in current frame"""

    # Current frame of Video Stream
    global frame

    # Modified frame for OpenCV
    global frameMod

    global running

    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    while running:

        # Check if frame has been initialized
        if len(frame):
            frameMod = frame.copy()

            # Create grayscale version of video feed for OpenCV
            grayscale = cv2.cvtColor(frameMod, cv2.COLOR_BGR2GRAY)

            # Create array of faces found using Haar Cascade face detection algorithm
            faces = faceCascade.detectMultiScale(grayscale, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frameMod, (x, y), (x + w, y + h), (0, 0, 255), 2)


if __name__ == '__main__':
    main()

