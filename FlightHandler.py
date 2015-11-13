import math

__author__ = 'Bryce Beagle'

# Import local libardrone from python-ardrone git clone
# Note: Renamed to python-ardrone to to avoid errors
from python_ardrone import libardrone

import cv2
import VariableHandler
import time

class Flight(object):

    def __init__(self):

        VariableHandler.drone.speed = .1
        VariableHandler.drone.takeoff()

        while VariableHandler.running:

            if VariableHandler.circles is None: continue

            # TODO: Update for line colors and altitude change
            if VariableHandler.circles[0] is not None:

                print "blah"

                distance = self.distanceFromCenter(VariableHandler.circles[0][0][0][0],
                                                   VariableHandler.circles[0][0][0][1])

                # if distance < 50:
                self.maintainAltitude()
                # else: print distance


    def maintainAltitude(self):

        desiredRadius = 200
        print "sds"

        if VariableHandler.circles[0][0][0][2] < desiredRadius - 30:
            print "Down"
            VariableHandler.drone.move_down()

        elif VariableHandler.circles[0][0][0][2] > desiredRadius + 30:
            print "Up"
            VariableHandler.drone.move_up()

        else:
            VariableHandler.drone.hover()
            print "Hover"

        time.sleep(.1)


    def followLine(self):

        pass

    def spin(self):

        pass

    def distanceFromCenter(self, x, y):

        screenCenterX = VariableHandler.bellyWidth  / 2
        screenCenterY = VariableHandler.bellyHeight / 2

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
