__author__ = 'Bryce Beagle'

from threading import Semaphore

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
