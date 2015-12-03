__author__ = 'Bryce Beagle'

from python_ardrone import libardrone

import VisionHandler
import DisplayHandler
import FlightHandler
import VariableHandler as vh


def main():

    # Use the belly camera
    libardrone.at_config(vh.drone.seq_nr + 1, "video:video_channel", 1)

    # Create a new instance of each subclass
    vh.Vision  = VisionHandler .Vision()
    vh.Display = DisplayHandler.Display()
    vh.Flight  = FlightHandler .Flight()

    # Start threads
    vh.Vision .start()
    vh.Display.start()
    vh.Flight .start()


if __name__ == "__main__" :
    main()