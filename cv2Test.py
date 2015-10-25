import cv2
from threading import Thread, Semaphore

# Create an instance of the Lock class
drawFrameSemaphore = Semaphore()
frameStepSemaphore = Semaphore()

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone


def main():
    """Main thread which handles getting video from Quadcopter Stream"""

    global frame, drawFrameMod, faces

    frontVideoIP = 'tcp://192.168.1.1:5555'

    # Should the program still be running
    global running
    running = True

    # Initialize frame, drawFrameMod, and faces to None to help mitigate race conditions
    frame, drawFrameMod, faces = None, None, None

    detectThread = Thread(target = detectFaces)
    drawThread   = Thread(target = drawFaces)

    detectThread.start()
    drawThread.start()

    # Get Video Stream from Quadcopter
    videoStream = cv2.VideoCapture(frontVideoIP)

    while running:
        # Get current frame of Video Stream
        running, frame = videoStream.read()

        frameStepSemaphore.release()

        if not running: break

        # Skip canvas drawing until first frame of Video Stream is found
        if drawFrameMod is None: continue

        drawFrameSemaphore.acquire()

        # Draw current frame to OpenCV window
        cv2.imshow('Video Stream', drawFrameMod)

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

    videoStream.release()
    cv2.destroyAllWindows()

    detectThread.join(1000)
    drawThread.join(1000)


def detectFaces():
    """Detect faces in current frame"""

    # Modified frame for use with OpenCV
    global frameMod, faces

    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    while running:

        # Skip face detection until first frame of Video Stream is found
        if frame is None: continue

        detectFrameMod = frame.copy()

        # Create grayscale version of video feed for OpenCV
        grayscale = cv2.cvtColor(detectFrameMod, cv2.COLOR_BGR2GRAY)

        # Create array of faces using Haar Cascade face detection algorithm
        faces = faceCascade.detectMultiScale(grayscale, 1.3, 5)


def drawFaces():

    global drawFrameMod

    while running:

        frameStepSemaphore.acquire()

        if frame is None or faces is None: continue

        drawFrameMod = frame.copy()

        for (x, y, w, h) in faces:
            cv2.rectangle(drawFrameMod, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Denote the current frame as finished
        drawFrameSemaphore.release()


if __name__ == '__main__':
    main()

