__author__ = 'Bryce Beagle'

import cv2


class ImageDraw(object):

    def __init__(self):
        pass


    def features(self, image, circles=None, triangles=None, lines=None, boxes=None):

        # Make a copy of passed image to prevent altering of original
        imageMod = image.copy()

        # If circles are requested
        if circles[0] is not None:

            # Draw circles
            imageMod = self.circles(imageMod, circles)

        # If triangles are requested
        if triangles is not None:

            # TODO: Draw triangles
            # Draw triangles
            imageMod = self.triangles(imageMod, triangles)

        if lines is not None:

            # Draw lines
            imageMod = self.lines(imageMod, lines)

        if boxes is not None:

            # TODO: Draw boxes
            # Draw boxes
            imageMod = self.boxes(imageMod, boxes)

        # Return modified image
        return imageMod


    def circles(self, imageMod, circles, centers=True):

        # TODO: Use **kwargs
        # TODO: Use filled param
        circleColor     = (255, 0, 0)
        centerColor     = (0, 0, 255)
        circleThickness = 2
        filled          = False

        # TODO: Implement filled circles
        for circle in circles[0][0]:

            # Draw circle
            cv2.circle(imageMod, (circle[0], circle[1]), circle[2], circleColor, circleThickness)

            # If circle centers are desired
            if centers is True:

                # Draw center point of circle
                cv2.circle(imageMod, (circle[0], circle[1]), 2, centerColor, 3)

        # Return image with circles drawn
        return imageMod


    def lines(self, imageMod, lines, lineColor, thickness=2):

        for x1, y1, x2, y2 in lines[0]:

            # Create origin and destination points
            origin      = (x1, y1)
            destination = (x2, y2)

            # Draw line from origin point to destination point
            cv2.line(imageMod, origin, destination, lineColor, thickness)

        return imageMod


    # TODO: Draw triangles
    def triangles(self, imageMod, triangles, centers=True):

        return imageMod


    # TODO: Draw boxes
    def boxes(self, imageMod, boxes):

        return imageMod
