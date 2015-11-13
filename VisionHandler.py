__author__ = 'Bryce Beagle'

import cv2
import VariableHandler

from threading import Thread
from OpenCVOps import ImageConvertLib, ImageSearchLib  # , FeatureTrackLib

# TODO: Fix boundingBoxes and circle detections overlap


class Vision(object):
    """Main thread which handles getting video from Quadcopter Stream"""

    def __init__(self):

        VariableHandler.drawFrameSemaphore.acquire()

        global convert, searchFor
        convert   = ImageConvertLib.ImageConvert()
        searchFor = ImageSearchLib .ImageSearch()

        identifyThread = Thread(target = self.identifyFeatures)
        identifyThread.start()

        # Video IP address and port that the ARDrone 2.0 uses to output the Video Stream
        videoIP = 'tcp://192.168.1.1:5555'

        # Get Video Stream from Quadcopter
        videoStream = cv2.VideoCapture(videoIP)

        while VariableHandler.running:

            # Get current frame of Video Stream
            VariableHandler.running, VariableHandler.frame = videoStream.read()

            # # Release the frame
            VariableHandler.frameStepSemaphore.release()

            # If no frame has been captured yet, continue
            if VariableHandler.frame is None: continue

            # Create a copy of the original frame to edit
            VariableHandler.frameMod = VariableHandler.frame.copy()


        # Release the video stream
        videoStream.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()

        VariableHandler.drone.reset()

    def identifyFeatures(self):

        # Acquire identifyFeaturesSemaphore to prevent other threads prematurely taking it first
        VariableHandler.identifyFeaturesSemaphore.acquire()

        while VariableHandler.running:

            # If no frame has been captured yet, continue
            if VariableHandler.frameMod is None: continue

            # Wait for a new frame
            VariableHandler.frameStepSemaphore.acquire()

            # Search for circles in the current isolated frame
            VariableHandler.circles = searchFor.features(VariableHandler.frame, circles = True)

            # Release the features for rendering to screen
            VariableHandler.identifyFeaturesSemaphore.release()
