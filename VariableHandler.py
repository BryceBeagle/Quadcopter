__author__ = 'Bryce Beagle'

from threading      import Event
from python_ardrone import libardrone

running = True

drone = libardrone.ARDrone()

# Threads
Display = None
Vision  = None
Flight  = None

# Features
circles     = None
circlesTemp = None
lines       = None
triangles   = None

# Modified Frames
frame         = None
frameMod      = None
isolatedFrame = None

# Events
frameStepEvent        = Event()
isolateColorEvent     = Event()
identifyFeaturesEvent = Event()
drawFrameEvent        = Event()

# Belly Camera Dimensions
bellyWidth  = 640
bellyHeight = 360

# Flight Constants
desiredX = bellyWidth  / 2
desiredY = bellyHeight / 2
desiredR = 75

# Current Positions
circleX = None
circleY = None
circleR = None

# Movement values
upDown          = 0
leftRight       = 0
forwardBackward = 0

horizontalTolerance = 0
verticalTolerance   = 0