import math

__author__ = 'Bryce Beagle'

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone

import cv2
import VariableHandler

class Flight(object):

    def __init__(self):

        global drone
        drone = libardrone.ARDrone()

        while VariableHandler.running:

            # TODO: Update for line colors and altitude change
            if VariableHandler.circles[0] is not None:

                if self.distanceFromCenter(VariableHandler.circles[0][0], VariableHandler.circles[0][1]) < 50:
                    self.maintainAltitude()


    def maintainAltitude(self):

        desiredRadius = 300

        if VariableHandler.circles[0][2] < desiredRadius - 30:
            drone.move(0, 0, 0, -0.1, 0)
        elif VariableHandler.circles[0][2] > desiredRadius + 30:
            drone.move(0, 0, 0,  0.1, 0)
        else: drone.hover()


    def followLine(self):

        pass

    def spin(self):

        pass

    def distance(self, x, y):

        length, height, _ =  VariableHandler.frame.shape

        screenCenterX = length / 2
        screenCenterY = height / 2

        distance = math.sqrt((screenCenterX - x)**2 + (screenCenterY - y)**2)

        return distance

#
#
#         If circles has a circle with center point at center of screen
#             If circle is orange
#                 Rotate 360 degrees CW
#             Else (circle must be blue)
#                 Rotate 360 degrees CCW
#             Mark circle as having been 'performed'
#
#         If triangles has a triangle with center point at center of screen
#             Shake
#             Mark triangle as having been performed
#
#         Follow line
#         If line is green
#             Ascend
#         If line is yellow
#             Maintain altitude
#         If line is red
#             Descend
