# import the necessary packages
from picamera import PiCamera
import time
import cv2
import numpy as np
from datetime import datetime
import logging

CHANNELS = 3


class PiCameraCapture:

    def __init__(self, framerate, width, height, *args, **kwargs):
        self.framerate = framerate
        self.width = width
        self.height = height
        self.classifier = cv2.CascadeClassifier(
            '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')

    def detect(self, collector, scale_factor, min_neighbors, min_size):
        logging.info('Starting detection')

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
                    minSize=tuple(min_size)
                )
                if len(faces) > 1:
                    logging.debug('Found {} faces', len(faces))
                data = (int(datetime.utcnow().timestamp() * 1000),
                        {"faces": len(faces)}, "picam")
                collector.collect(data)

                # Draw a rectangle around the faces
                # for (x, y, w, h) in faces:
                #    cv2.rectangle(frame, (x, y), (x + w, y + h),
                #                  (0, 255, 0), 2)
                #    cv2.imwrite("face-%d.jpg" % d, frame)

                #cv2.imwrite("frame.jpg", frame)
