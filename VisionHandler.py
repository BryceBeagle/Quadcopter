__author__ = 'Bryce Beagle'

import cv2
import VariableHandler as vh

from threading import Thread
from OpenCVOps import ImageConvertLib, ImageSearchLib


# TODO: Fix boundingBoxes and circle detections overlap


class Vision(Thread):
    """Main thread which handles getting video from Quadcopter Stream"""
    
    def run(self):

        # Video IP address and port that the ARDrone 2.0 uses to output the Video Stream
        videoIP = 'tcp://192.168.1.1:5555'

        global convert, searchFor
        convert   = ImageConvertLib.ImageConvert()
        searchFor = ImageSearchLib .ImageSearch()

        identifyThread = Thread(target = self.identifyFeatures)
        identifyThread.start()

        # Get Video Stream from Quadcopter
        videoStream = cv2.VideoCapture(videoIP)

        while vh.running:

            # Get current frame of Video Stream
            vh.running, vh.frame = videoStream.read()

            # Release the frame and immediately lock the next
            vh.frameStepEvent.set()
            vh.frameStepEvent.clear()

            # If no frame has been captured yet, continue
            if vh.frame is None: continue

            # Create a copy of the original frame to edit
            vh.frameMod = vh.frame.copy()

        # Release the video stream
        videoStream.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()

    def identifyFeatures(self):

        while vh.running:

            # If no frame has been captured yet, continue
            if vh.frameMod is None: continue

            # Wait for a new frame to be released
            vh.frameStepEvent.wait()

            # Search for circles in the current isolated frame
            vh.circlesTemp = searchFor.features(vh.frame, circles = True)

            # Extract the circles from the unnecessary surrounding layers
            if vh.circlesTemp[0] is not None:
                vh.circles = vh.circlesTemp[0][0]

            # Release the features for rendering to screen and immediately lock them again
            vh.identifyFeaturesEvent.set()
            vh.identifyFeaturesEvent.clear()
