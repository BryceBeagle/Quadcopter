__author__ = 'Bryce Beagle'

import VariableHandler as vh
import math

from threading import Thread


class Flight(Thread):

    def run(self):

        # # Ensure that the Quadcopter is not in an Emergency Stop state
        # vh.drone.reset()

        # Wait for camera
        vh.frameStepEvent.wait()

        # Takeoff
        vh.drone.takeoff()

        while vh.running:

            # Wait for Features to be processed at least once
            vh.identifyFeaturesEvent.wait()

            if vh.circles is None: continue

            # TODO: Update for line colors and altitude change
            # TODO: Slow down checks to once per frame
            if vh.circles[0] is not None:

                # vh.drone.land()
                self.preciseMaintainAltitude()
                # self.maintainAltitude()

            else:
                vh.drone.hover()

        # When the program ends, land the quadcopter
        vh.drone.land()
        vh.drone.halt()

    def maintainAltitude(self):

        CircleX = vh.circles[0][0]
        CircleY = vh.circles[0][1]
        CircleR = vh.circles[0][2]

        # Vertical Movement
        if CircleR < vh.desiredR - vh.horizontalTolerance:
            print "Down",
            vh.upDown = -1
        elif CircleR > vh.desiredR + vh.horizontalTolerance:
            print "Up",
            vh.upDown = 1
        else:
            print "Hover Vertically",
            vh.upDown = 0

        # Left-Right Movement
        if CircleX < ((vh.bellyWidth / 2) - vh.horizontalTolerance):
            print "Right",
            vh.leftRight = 1
        elif CircleX > ((vh.bellyWidth / 2) + vh.horizontalTolerance):
            print "Left",
            vh.leftRight = -1
        else:
            print "Hover Laterally",
            vh.leftRight = 0

        # Forward-Backward Movement
        if CircleY < ((vh.bellyHeight / 2) - vh.verticalTolerance):
            print "Backward"
            vh.forWardBackward = -1
        elif CircleY > ((vh.bellyHeight / 2) + vh.verticalTolerance):
            print "Forward"
            vh.forwardBackward = 1
        else:
            print "Hover Horizontally"
            vh.forwardBackward = 0

        # Move drone
        vh.drone.move(vh.leftRight, vh.forwardBackward, vh.upDown, 0)

    def preciseMaintainAltitude(self):

        # Get first (best) circle from circle array
        vh.circleX = vh.circles[0][0]
        vh.circleY = vh.circles[0][1]
        vh.circleR = vh.circles[0][2]

        self.setSpeed(vh.circleX, vh.circleY, vh.circleR)

        # Move drone
        vh.drone.move(vh.leftRight, vh.forwardBackward, vh.upDown, 0)

        # print "Left-Right:", vh.leftRight,
        # print "Forward-Backward:", vh.forwardBackward,
        # print "Up-Down:", vh.upDown


    # TODO: Convert to lambda
    # TODO: Move to library
    def setSpeed(self, circleX, circleY, circleR):

        distanceX, distanceY, distanceR = self.distanceFromCenter(circleX, circleY, circleR)

        proportionalDistanceX = distanceX / vh.desiredR
        proportionalDistanceY = distanceY / vh.desiredR
        proportionalDistanceV = distanceR / vh.desiredR

        # print "Distance P X:", proportionalDistanceX,
        # print "Distance P Y:", proportionalDistanceY,
        # print "Distance P R:", proportionalDistanceV

        vh.leftRight       =  .05 * math.atan(proportionalDistanceX * .4) / (math.pi / 2) - .015
        vh.forwardBackward =  .05 * math.atan(proportionalDistanceY * .4) / (math.pi / 2)
        vh.upDown          =  .4  * math.atan(proportionalDistanceV * .4) / (math.pi / 2) - .01


    def distanceFromCenter(self, circleX, circleY, circleR):

        screenCenterX = vh.bellyWidth  / 2
        screenCenterY = vh.bellyHeight / 2

        distanceX = circleX - screenCenterX
        distanceY = circleY - screenCenterY
        distanceR = circleR - vh.desiredR

        return distanceX, distanceY, distanceR

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
