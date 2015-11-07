__author__ = 'Bryce Beagle'

from OpenCVOps import ImageTransformLib, ImageSearchLib
import cv2

# TODO: Implement values in ImageTransformLib
colorBoundaries = {"Red"   : ([350, 100, 100], [ 10, 255, 255]),
                   "Green" : ([110, 100, 100], [130, 255, 255]),
                   "Blue"  : ([230, 100, 100], [250, 255, 255])}


convert   = ImageTransformLib.ImageTransform()
searchFor = ImageSearchLib.ImageSearch()

def main():

    testImage = cv2.imread('TestLine.jpg')

    isolatedTestImage = isolateColor(testImage, "Green")
    circles = identifyFeatures(testImage, circles=True)[0]

    drawFeatures(testImage, circles)


def isolateColor(testImage, color):
    """Attempts to find a line of the specified color in the supplied image."""

    # Create a new window to display output
    cv2.namedWindow("Isolated Color with Identified Features", cv2.WINDOW_NORMAL)

    # Isolate the specified color in the test image
    testImageColor    = convert.RGBtoHSVRange(colorBoundaries[color])
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

    print circles

    if circles is not None:

        print "Circles:\n", circles

        for i in circles[0]:

            print "i:\n", i

            # Draw the circle
            cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 2)
            # Draw the center point of the circle
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow("Isolated Color with Identified Features", image)

    running = True

    print "lol"

    while running:

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False




if __name__ == '__main__':
    main()
