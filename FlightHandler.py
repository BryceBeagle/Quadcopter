__author__ = 'Bryce Beagle'

import VariableHandler as vh

from threading import Thread


class Flight(Thread):

    def run(self):

        vh.drone.takeoff()

        while vh.running:

            navdata = vh.drone.navdata
            print navdata

            # Wait for Features to be processed at least once
            vh.identifyFeaturesEvent.wait()

            if vh.circles is None: continue

            # TODO: Update for line colors and altitude change
            # TODO: Slow down checks to once per frame
            if vh.circles[0] is not None:

                navdata = vh.drone.navdata
                print navdata

                # vh.drone.land()
                self.maintainAltitude()

            else:
                vh.drone.hover()

        vh.drone.land()
        vh.drone.halt()


    def maintainAltitude(self):

        CircleX = vh.circles[0][0]
        CircleY = vh.circles[0][1]
        CircleR = vh.circles[0][2]

        print CircleX, CircleY, CircleR

        # Vertical Movement
        if CircleR < vh.desiredHoverRadius - vh.horizontalTolerance:
            print "Down",
            vh.upDown = -1
        elif CircleR > vh.desiredHoverRadius + vh.horizontalTolerance:
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

    # def distanceFromCenter(self, x, y):
    #
    #     screenCenterX = vh.bellyWidth  / 2
    #     screenCenterY = vh.bellyHeight / 2
    #
    #     distance = math.sqrt((screenCenterX - x)**2 + (screenCenterY - y)**2)
    #
    #     return distance

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
