__author__ = 'Bryce Beagle'

from threading      import Semaphore
from python_ardrone import libardrone

running       = True

circles       = None
lines         = None
triangles     = None

frame         = None
frameMod      = None
isolatedFrame = None

# Create semaphores
frameStepSemaphore        = Semaphore()
isolateColorSemaphore     = Semaphore()
identifyFeaturesSemaphore = Semaphore()
drawFrameSemaphore        = Semaphore()

drone = libardrone.ARDrone()

# Belly Camera Dimensions
bellyWidth  = 360
bellyHeight = 640
