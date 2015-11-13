__author__ = 'Bryce Beagle'

import cv2

from OpenCVOps import ImageConvertLib, ImageSearchLib
from OpenCVOps.ColorConstants import Colors, ColorRanges

convert   = ImageConvertLib.ImageConvert()
searchFor = ImageSearchLib.ImageSearch()

def main():

    testImage = cv2.imread('TestLine.jpg')

    isolatedTestImage = isolateColor(testImage, ColorRanges.GREEN_RANGE)
    circles = identifyFeatures(testImage, circles=True)[0]

    drawFeatures(testImage, circles)


def isolateColor(testImage, colorRange):
    """Attempts to find a line of the specified color in the supplied image."""

    # Create a new window to display output
    cv2.namedWindow("Isolated Color with Identified Features", cv2.WINDOW_NORMAL)

    # Isolate the specified color in the test image
    testImageColor    = convert.RGBtoHSVRange(colorRange)
    isolatedTestImage = convert.toColorRange(testImage, testImageColor)

    return isolatedTestImage


def identifyFeatures(image, circles=None, triangles=None):

    # TODO: Return only passed parameters

    identifiedCircles = identifiedTriangles = None

    if circles is not None:

        identifiedCircles = searchFor.HoughCircles(image)

    if triangles is not None:

        # TODO: Identify triangles
        identifiedTriangles = None

    return identifiedCircles, identifiedTriangles


def drawFeatures(image, circles=None, triangles=None):

    if circles is not None:

        for i in circles[0]:

            # Draw the circle
            cv2.circle(image, (i[0], i[1]), i[2], Colors.RED, 2)
            # Draw the center point of the circle
            cv2.circle(image, (i[0], i[1]), 2, Colors.GREEN, 3)

    cv2.imshow("Isolated Color with Identified Features", image)

    running = True

    while running:

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False




if __name__ == '__main__':
    main()
