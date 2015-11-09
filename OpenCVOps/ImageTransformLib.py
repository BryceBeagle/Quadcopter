from OpenCVOps.ColorConstants import Colors

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


    def toHSV(self, image, conversionType=cv2.COLOR_BGR2HSV):
        """
        Convert a BGR Image to HSV.
        Yeah, this function is pretty useless.
        """

        return cv2.cvtColor(image, conversionType)


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

        # Get a mask containing all pixels that fall within the Color Range
        mask = cv2.inRange(HSVImage, lowerHSV, upperHSV)

        # Combine the original picture with the mask using a bitwise-and
        colorRangeImage = cv2.bitwise_and(image, image, mask=mask)

        return colorRangeImage


    def onlyColors(self, image):

        # Isolate all three Color Bands
        redChannel   = self.toColorRange(image, Colors.RED)
        greenChannel = self.toColorRange(image, Colors.GREEN)
        blueChannel  = self.toColorRange(image, Colors.BLUE)

        # Combined all three Isolated Color Band images
        colorizedImage = cv2.bitwise_or(cv2.bitwise_or(redChannel, greenChannel), blueChannel)

        return colorizedImage


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
