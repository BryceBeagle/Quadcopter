from OpenCVOps import ImageTransformLib
import cv2

#colorBoundaries = {"Red"   : ([350, 100, 100], [ 10, 255, 255]),
#                   "Green" : ((110, 100, 100], [130, 255, 255]),
#                   "Blue"  : ([230, 100, 100], [250, 255, 255])}



convert = ImageTransformLib.ImageTransform()


def main():

    testImage = cv2.imread('TestLine.jpg')

    getLine(testImage, "Green")


def getLine(testImage, color):
    """Attempts to find a line of the specified color in the supplied image."""



    #testImageColor = convert.toColorRange(testImage, np.array([110, 100, 100]), np.array([130, 255, 255]))

    cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
    cv2.imshow("Test", testImageColor)



    running = True

    while running:

        # Wait for escape character (Escape Key) to be pressed. Once pressed, OpenCV window is closed
        if cv2.waitKey(1) & 0xFF == 27:
            running = False

if __name__ == '__main__':
    main()