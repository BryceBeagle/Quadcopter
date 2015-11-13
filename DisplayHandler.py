__author__ = 'Bryce Beagle'

import VariableHandler

from OpenCVOps import ImageDrawLib

# TODO: Remove all direct references to cv2
import cv2


class Display(object):

    def __init__(self):

        global draw
        draw = ImageDrawLib.ImageDraw()

        while VariableHandler.running:

            self.drawFeatures()


    def drawFeatures(self):

        while VariableHandler.running:

            VariableHandler.frameStepSemaphore.acquire()
            # VariableHandler.drawFrameSemaphore.acquire()

            # Skip canvas drawing until first frame of Video Stream is found
            if VariableHandler.frameMod is None:
                continue

            if VariableHandler.circles is not None:

                # Draw features on current frame
                VariableHandler.frameMod = draw.features(VariableHandler.frameMod,
                                                         circles=VariableHandler.circles)

            # Otherwise, show unmodified Video Stream
            else: VariableHandler.frameMod = VariableHandler.frame

            # Draw current modified frame to OpenCV window
            cv2.imshow('Video Stream', VariableHandler.frameMod)

            # Look for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
            if cv2.waitKey(1) & 0xFF == 27: VariableHandler.running = False

            # Allow the Feature Detection thread to grab another frame
            VariableHandler.drawFrameSemaphore.release()
