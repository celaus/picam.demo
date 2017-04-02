# import the necessary packages
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture


CHANNELS = 3

class PiCameraCapture:

    def __init__(self, framerate, width, height, *args, **kwargs):
        self.framerate = framerate
        self.width = width
        self.height = height
        self.classifier = cv2.CascadeClassifier(
            '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

    def detect(self, collector, scale_factor, min_neighbors, min_size):
        with PiCamera(resolution=(self.width, self.height), framerate=self.framerate) as camera:
            stream = np.empty(
                (self.height * self.width * CHANNELS), dtype=np.uint8)
            # capture frames from the camera
            d = 0
            for raw in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                d += 1
                stream = stream.reshape((self.height, self.width, CHANNELS))

                frame = stream
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.classifier.detectMultiScale(
                    gray,
                    scaleFactor=scale_factor,
                    minNeighbors=min_neighbors,
                    minSize=min_size
                )
                collector.collect()
                # Draw a rectangle around the faces
                #for (x, y, w, h) in faces:
                #    cv2.rectangle(frame, (x, y), (x + w, y + h),
                #                  (0, 255, 0), 2)
                #    cv2.imwrite("face-%d.jpg" % d, frame)

                #cv2.imwrite("frame.jpg", frame)
