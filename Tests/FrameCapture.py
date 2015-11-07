__author__ = 'ignormies'

import cv2
from python_ardrone import libardrone

drone = libardrone.ARDrone()


def main():

    running = True

    # Use the belly camera
    libardrone.at_config(drone.seq_nr + 1, "video:video_channel", 1)

    # Default IP Address and
    frontVideoIP = 'tcp://192.168.1.1:5555'

    # Get Video Stream from Quadcopter
    videoStream = cv2.VideoCapture(frontVideoIP)


    while running:

        # Get current frame of Video Stream
        running, frame = videoStream.read()

        if not running: break

        # Draw current frame to OpenCV window
        cv2.imshow('Video Stream', frame)

        # Get currently pressed key
        ch = cv2.waitKey(1)

        # Convert ascii to character. The (ch == -1)*256 is to fix a bug
        keyPressed = chr(ch + (ch == -1) * 256).lower().strip()

        # If the Esc Key is pressed, the OpenCV window is closed
        if keyPressed == chr(27): running = False

        # If 'c' is pressed, the current frame is saved locally
        if keyPressed == 'c': cv2.imwrite(frame)


if __name__ == '__main__':
    main()