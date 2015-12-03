__author__ = 'Bryce Beagle'

import VariableHandler as vh

from threading import Thread
from OpenCVOps import ImageDrawLib

# TODO: Remove all direct references to cv2
import cv2


class Display(Thread):

    def run(self):

        global draw
        draw = ImageDrawLib.ImageDraw()

        while vh.running:

            self.drawFeatures()


    def drawFeatures(self):

        while vh.running:

            # Wait for a new frame to be released
            vh.frameStepEvent.wait()

            # Skip canvas drawing until first frame of Video Stream is found
            if vh.frameMod is None: continue

            if vh.circles is not None:

                # Draw features on current frame
                vh.frameMod = draw.features(vh.frameMod, circles=vh.circles)

            # Otherwise, show unmodified Video Stream
            else: vh.frameMod = vh.frame

            # Draw current modified frame to OpenCV window
            cv2.imshow('Video Stream', vh.frameMod)

            # TODO: Turn key input into case-switch

            # Look for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
            if cv2.waitKey(1) & 0xFF == 27:

                print "Closing"
                vh.running = False

                # Unblock all Events in case a thread is stuck waiting for one
                vh.frameStepEvent       .set()
                vh.isolateColorEvent    .set()
                vh.identifyFeaturesEvent.set()
                vh.drawFrameEvent       .set()

            # Allow the Feature Detection thread to grab another frame and immediately lock the next
            vh.drawFrameEvent.set()
            vh.drawFrameEvent.clear()
