__author__ = 'Bryce Beagle'

import cv2
import numpy as np
import ImageConvertLib

convert = ImageConvertLib.ImageConvert()


class FeatureTrack(object):

    def __init__(self): pass

    def circle(self, frame, boundingBox, boxMargins=0):

        # Convert roiPoints to a numpy array
        np.array(boundingBox)

        # Initialize the termination criteria for camShift
        # Ten iterations looking for a movement of at least one pixel
        termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

        # Get the top left and bottom right corners from the bounding box
        topLeftCorner     = boundingBox[0]
        bottomRightCorner = boundingBox[2]

        # Grab the Region of Interest from the current frame
        regionOfInterest = frame[topLeftCorner[1]:bottomRightCorner[1],
                                 topLeftCorner[0]:bottomRightCorner[0]]
        regionOfInterest = convert.toHSV(regionOfInterest)

        # Calculate a histogram for the Region of Interest
        regionHistogram = cv2.calcHist([regionOfInterest], [0], None, [16], [0, 180])
        regionHistogram = cv2.normalize(regionHistogram, alpha=0, beta=255, cv2.NORM_MINMAX)

        if boundingBox is not None:

            # Convert the current frame to HSV
            HSVFrameMod = convert.toHSV(frame)

            # Perform mean shift algorithm
            backProjection = cv2.calcBackProject([HSVFrameMod], [0], regionHistogram, [0, 180], 1)

            # Apply CamShift algorithm to back projection
            (corners, boundingBox) = cv2.CamShift(backProjection, boundingBox, termination)

            return corners, boundingBox

        return boundingBox,

