__author__ = 'Bryce Beagle'

import cv2
import numpy as np

class ImageTransform(object):
    """ Image Transformation Class

    Performs image transformations.
    """

    def __init__(self):

        # Color names and ranges
        self.colorValues = {"Red"   : [255,   0,   0],
                            "Green" : [  0, 255,   0],
                            "Teal"  : [  0, 255, 212],
                            "Blue"  : [  0,   0, 255]}


    def toGrayscale(self, image):
        """"Convert a BGR image to grayscale."""

        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    def toHSV(self, image):
        """Convert a BGR Image to HSV."""

        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    def RGBtoHSVRange(self, color):
        """Convert an array containing RGB values to numpy arrays representing a range of HSV values."""

        # TODO: Turn into **kwargs
        # Default HSV color ranges
        hueRange      = 10
        minSaturation = 100
        maxSaturation = 255
        minValue      = 100
        maxValue      = 255

        # TODO: Implement direct conversion of RGB images using COLOR_RGB2HSV

        # Convert color to a 3 dimensional uint8 array
        colorRGB = np.uint8([[color]])

        # Convert the RGB array to an HSV array
        colorHSV = cv2.cvtColor(colorRGB, cv2.COLOR_RGB2HSV)

        # Create the upper and lower bounds for the color range
        lowerHSV = np.array([colorHSV[0][0][0] - hueRange, minSaturation, minValue])
        upperHSV = np.array([colorHSV[0][0][0] + hueRange, maxSaturation, maxValue])

        # Return a tuple containing the upper and lower bound for the range
        return lowerHSV, upperHSV

    def toColorRange(self, image, (lowerHSV, upperHSV)):
        """Convert a BGR Image to an image containing only values in a specific RGB color range."""

        # Convert image to HSV
        HSVImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(HSVImage, lowerHSV, upperHSV)

        return cv2.bitwise_and(image, image, mask=mask)

    def onlyColors(self, image):

        # Convert image to HSV
        HSVImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    def toSmooth(self, image, blurType, ):
        pass


    def toSkeleton(self, image):

        imageSize = np.size(image)
        skeleton  = np.zeros(image.shape, np.uint8)

        ret, image = cv2.threshold(image, 127, 255, 0)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        done = False

        while not done:

            eroded   = cv2.erode     (image,    element)
            temp     = cv2.dilate    (eroded,   element)
            temp     = cv2.subtract  (image,    temp)
            skeleton = cv2.bitwise_or(skeleton, temp)
            image    = eroded.copy()

            print "Image Size:", imageSize
            print "CountNonZero:", cv2.countNonZero(image)

            zeros = imageSize - cv2.countNonZero(image)
            if zeros == imageSize:
                done = True

        return skeleton
