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
bellyWidth  = 360
bellyHeight = 640

# Flight Constants
desiredHoverRadius  = 100
hoverTolerance      = 20
horizontalTolerance = 0
verticalTolerance   = 0

# Movement values
upDown          = 0
leftRight       = 0
forwardBackward = 0
