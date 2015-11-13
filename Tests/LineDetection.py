__author__ = 'Bryce Beagle'

import cv2

from OpenCVOps import ImageConvertLib, ImageSearchLib, ImageDrawLib
from OpenCVOps.ColorConstants import Colors

convert   = ImageConvertLib.ImageConvert()
searchFor = ImageSearchLib.ImageSearch()
draw      = ImageDrawLib.ImageDraw()


def main():

    testImage = cv2.imread('LineTest.png')

    testImageMod = convert.toOnlyColors(testImage)

    cv2.imshow('Blah', testImageMod)

    running = True
    while running:

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

    lines = searchFor.HoughLinesP(testImageMod, minLineLength=100, maxLineGap=20)
    testImageMod = draw.lines(testImage, lines, Colors.GREEN)

    cv2.imshow('Blah', testImageMod)

    running = True
    while running:

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False




if __name__ == '__main__':
    main()
