__author__ = 'Bryce Beagle'

import cv2
from OpenCVOps import ImageTransformLib

convert = ImageTransformLib.ImageTransform()


class ImageSearch(object):

    def __init__(self):
        pass


    def features(self, image, circles=False, triangles=False):

        # TODO: Return only passed parameters

        # Initialize identifiedCircles and identifiedTriangles
        identifiedCircles = identifiedTriangles = None

        # If circles are requested
        if circles is True:

            # Search for circles
            identifiedCircles = self.HoughCircles(image)

        # If triangles are requested
        if triangles is True:

            # TODO: Identify triangles
            # Search for triangles
            identifiedTriangles = None

        # Return identified circles and triangles
        return identifiedCircles, identifiedTriangles


    def HoughCircles(self, image):

        # TODO: Use **kwargs
        dp = 1
        minDst = 50
        param1 = 20
        minRadius = 100
        maxRadius = 400

        # Initialize circles
        circles = None

        # TODO: Don't try converting already grayscale images

        # Convert image to grayscale
        imageGrayscale = convert.toGrayscale(image)

        # Slightly blur image to reduce
        imageBlurred = cv2.GaussianBlur(imageGrayscale, (7, 7), 0)

        # Keep attempting stricter and stricter searches until at most two circles are found
        for i in xrange (60, 200, 10):

            # Store detected circles in a temp variable in case current iteration finds no circles
            circlesTemp = cv2.HoughCircles(imageBlurred, cv2.cv.CV_HOUGH_GRADIENT,
                                           dp, minDst, None,
                                           param1, i,
                                           minRadius, maxRadius)

            # If HoughCircles algorithm found circles, store them
            if circlesTemp is not None: circles = circlesTemp

            # If HoughCircles algorithm did not find circles, return previous iteration of circles (or None in the event
            #   that circles were not found in first iteration). Any further attempts using stricter search parameters
            #   will not find circles
            else: return circles

            # If fewer than 3 circles were found, return them
            if len(circles[0]) < 3 or circles is None: return circles

        return circles
