import cv2
from threading import Thread

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone


def main():
    """Main thread which handles getting video from Quadcopter Stream"""

    global frame
    global frameMod
    global currentState
    currentState = 0

    videoIP = 'tcp://192.168.1.1:5555'

    # Should the program still be running
    global running
    running = True

    # Initialize frame and frameMod to None to help mitigate race conditions
    frame, frameMod = None, None

    robotThread = Thread(target = detectFaces)
    robotThread.start()

    # Get Video Stream from Quadcopter
    videoStream = cv2.VideoCapture(videoIP)

    while running:
        # Get current frame of Video Stream
        running, frame = videoStream.read()

        if not running: break

        # Skip canvas drawing until first frame of Video Stream is found
        if frameMod is None: continue

        # Draw current frame to OpenCV window
        cv2.imshow('Video Stream', frameMod)
        print currentState

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

    videoStream.release()
    cv2.destroyAllWindows()

    robotThread.join(1000)


def detectFaces():
    """Detect faces in current frame"""

    # Modified frame for use with OpenCV
    global frameMod

    global currentState

    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    while running:

        # Skip face detection until first frame of Video Stream is found
        if frame is None: continue

        currentState = 1

        frameMod = frame.copy()

        currentState = 2

        # Create grayscale version of video feed for OpenCV
        grayscale = cv2.cvtColor(frameMod, cv2.COLOR_BGR2GRAY)

        currentState = 3

        # Create array of faces found using Haar Cascade face detection algorithm
        faces = faceCascade.detectMultiScale(grayscale, 1.3, 5)

        currentState = 4

        for (x, y, w, h) in faces:
            cv2.rectangle(frameMod, (x, y), (x + w, y + h), (0, 0, 255), 2)

        currentState = 5

if __name__ == '__main__':
    main()

