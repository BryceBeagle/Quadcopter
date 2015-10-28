import cv2
from threading import Thread, Semaphore

from OpenCVOps import ImageTransformLib

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone

# Create semaphores
drawFrameSemaphore = Semaphore()
frameStepSemaphore = Semaphore()

convert = ImageTransformLib.ImageTransform()

drone = libardrone.ARDrone()


def main():
    """Main thread which handles getting video from Quadcopter Stream"""

    # Use the belly camera
    libardrone.at_config(drone.seq_nr + 1, "video:video_channel", 1)


    global frame, drawFrameMod, faces

    frontVideoIP = 'tcp://192.168.1.1:5555'

    # Should the program still be running
    global running
    running = True

    # Initialize frame, drawFrameMod, and faces to None to help mitigate race conditions
    frame, drawFrameMod, faces = None, None, None

    isolateThread = Thread(target = isolateColor)
    isolateThread.start()

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

        print drawFrameMod

        # Draw current frame to OpenCV window
        cv2.imshow('Video Stream', drawFrameMod)

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

    videoStream.release()
    cv2.destroyAllWindows()

    isolateThread.join(1)

def isolateColor():

        global drawFrameMod

        while running:

            frameStepSemaphore.acquire()

            if frame is None: continue

            detectFrameMod = frame.copy()

            print detectFrameMod

            drawFrameMod = convert.toColorRange(detectFrameMod, convert.RGBtoHSVRange(convert.colorValues["Teal"]))

            drawFrameSemaphore.release()

if __name__ == '__main__':
    main()


