__author__ = 'Bryce Beagle'

from threading      import Thread
from python_ardrone import libardrone

import FlightHandler
import VisionHandler
import DisplayHandler
import VariableHandler


def main():

    # Use the belly camera
    libardrone.at_config(VariableHandler.drone.seq_nr + 1, "video:video_channel", 1)

    # Create threads for each routine
    visionThread  = Thread(target = Vision)
    flightThread  = Thread(target = Flight)
    displayThread = Thread(target = Display)

    # Start threads
    visionThread .start()
    flightThread .start()
    displayThread.start()


def Vision():

    VisionHandler.Vision()


def Display():

    DisplayHandler.Display()


def Flight():

    FlightHandler.Flight()


if __name__ == "__main__" :
    main()