__author__ = 'Bryce Beagle'

import cv2
import numpy as np


class ImageTransform(object):
    """ Image Transformation Class

    Performs image transformations.
    """

    def __init__(self):
        pass


    def toGrayscale(self, image):
        """"Convert a BGR image to grayscale."""

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    def toHSV(self, image):
        """Convert a BGR Image to HSV."""

        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    def RGBtoHSVRange(self, colorRGB, hueRange=10, minSat=100, maxSat=255, minVal=100, maxVal=255):
        """Convert an array containing RGB values to numpy arrays representing a range of HSV values."""

        print colorRGB

        colorBGR = np.uint8([[colorRGB[::-1]]])

        print colorBGR

        colorHSV = cv2.cvtColor(colorBGR, cv2.COLOR_BGR2HSV)
        colorHSV = [[[colorHSV[[[0]]] * 2, colorHSV[[[1]]], colorHSV[[[2]]]]]]
        print colorHSV

        lowerHSV = np.array([[[colorHSV[0][0][0] - hueRange, minSat, minVal]]])
        upperHSV = np.array([[[colorHSV[0][0][0] + hueRange, maxSat, maxVal]]])

        return lowerHSV, upperHSV

    def toColorRange(self, image, (lowerHSV, upperHSV)):
        """Convert a BGR Image to an image containing only values in a specific RGB color range."""

        # Convert image to HSV
        HSVImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(HSVImage, lowerHSV, upperHSV)

        return cv2.bitwise_and(image, image, mask=mask)


    def toSkeleton(self, image):

        imageSize = np.size(image)
        skeleton  = np.zeros(image.shape, np.uint8)

        ret, image = cv2.threshold(image, 127, 255, 0)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        done = False

        while not done:

            eroded = cv2.erode(image, element)
            temp = cv2.dilate(eroded, element)
            temp = cv2.subtract(image, temp)
            skeleton = cv2.bitwise_or(skeleton, temp)
            image = eroded.copy()

            zeros = imageSize - cv2.countNonZero(image)
            if zeros == imageSize:
                done = True

        return skeleton
