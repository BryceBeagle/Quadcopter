import cv2
from threading import Thread, Semaphore

from OpenCVOps import ImageTransformLib, ImageSearchLib, ImageDrawLib

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone

# Create semaphores
frameStepSemaphore        = Semaphore()
isolateColorSemaphore     = Semaphore()
identifyFeaturesSemaphore = Semaphore()
drawFrameSemaphore        = Semaphore()


convert   = ImageTransformLib.ImageTransform()
searchFor = ImageSearchLib.ImageSearch()
draw      = ImageDrawLib.ImageDraw()

drone     = libardrone.ARDrone()


def main():
    """Main thread which handles getting video from Quadcopter Stream"""

    global frame, drawFrameMod, isolatedFrameMod
    global faces, circles

    # Variable to alert threads that the should or should not be still running
    global running
    running = True

    # Use the belly camera
    libardrone.at_config(drone.seq_nr + 1, "video:video_channel", 1)

    # Video IP address and port that the ARDrone 2.0 uses to output the Video Stream
    videoIP = 'tcp://192.168.1.1:5555'

    # Initialize frame, drawFrameMod, and isolateFrameMod to None to help mitigate race conditions
    frame, drawFrameMod, isolatedFrameMod = None, None, None

    # Initialize faces and circles to None
    faces, circles = None, None

    # Create threads
    isolateThread  = Thread(target = isolateColor)
    identifyThread = Thread(target = identifyFeatures)
    drawThread     = Thread(target = drawFeatures)

    # Start threads
    isolateThread.start()
    identifyThread.start()
    drawThread.start()

    # Get Video Stream from Quadcopter
    videoStream = cv2.VideoCapture(videoIP)

    while running:

        # Get current frame of Video Stream
        running, frame = videoStream.read()

        # Release the frame
        frameStepSemaphore.release()

        # Break if Video Stream is lost
        if not running: break

        # Skip canvas drawing until first frame of Video Stream is found
        if drawFrameMod is None: continue

        # Wait for next frame to be modified
        drawFrameSemaphore.acquire()

        # Draw current modified frame to OpenCV window
        cv2.imshow('Video Stream', drawFrameMod)

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False


    # Release the video stream
    videoStream.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

    # Merge all threads back together
    isolateThread.join(1)
    identifyThread.join(1)
    drawThread.join(1)


def isolateColor():

        global isolatedFrameMod

        # Acquire isolateColorSemaphore to prevent other threads prematurely taking it first
        isolateColorSemaphore.acquire()

        while running:

            # Wait for next frame to be acquired
            frameStepSemaphore.acquire()

            if frame is None: continue

            # Make a copy of the active frame to prevent altering of original
            frameMod = frame.copy()

            # Isolate the color Teal from the current frame
            testImageColor   = convert.RGBtoHSVRange(([110, 100, 100], [130, 255, 255]))
            isolatedFrameMod = convert.toColorRange(frameMod, testImageColor)

            # Release the Isolated Color frame
            isolateColorSemaphore.release()


def identifyFeatures():

    global circles

    # Acquire identifyFeaturesSemaphore to prevent other threads prematurely taking it first
    identifyFeaturesSemaphore.acquire()

    while running:

        # Wait for latest Isolated Color frame
        isolateColorSemaphore.acquire()

        # Search for circles in Isolated Color frame
        circles = searchFor.features(isolatedFrameMod, True)

        print circles

        # Release the features
        identifyFeaturesSemaphore.release()


def drawFeatures():

    global drawFrameMod

    # Acquire drawFrameSemaphore to prevent other threads prematurely taking it first
    drawFrameSemaphore.acquire()

    # Wait for frame to draw on
    isolateColorSemaphore.acquire()

    while running:

        # Wait for features to be identified in latest frame
        identifyFeaturesSemaphore.acquire()

        if circles[0] is not None:

            # Draw features on current frame
            drawFrameMod = draw.features(isolatedFrameMod, circles)

        else: drawFrameMod = frame

        # Release the modified frame
        drawFrameSemaphore.release()




# def createSkeleton():
#
#     global drawFrameMod
#
#     while running:
#
#         isolateColorSemaphore.aquire()
#
#         if drawFrameMod is None: continue
#
#         drawFrameMod = convert.toSkeleton(drawFrameMod)
#
#         drawFrameSemaphore.release()


if __name__ == '__main__':
    main()

