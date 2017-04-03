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
        self.last_frame = None
        self._stop = False

    def stop(self):
        self._stop = True

    def detect(self, collector, scale_factor, min_neighbors, min_size):
        logging.info('Starting detection')
        frames = 0
        start = int(datetime.utcnow().timestamp() * 1000)
        try:
            with PiCamera(resolution=(self.width, self.height), framerate=self.framerate) as camera:
                stream = np.empty(
                    (self.height * self.width * CHANNELS), dtype=np.uint8)
                # capture frames from the camera
                for raw in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                    frames += 1
                    stream = stream.reshape((self.height, self.width, CHANNELS))

                    frame = stream
                    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # faces = self.classifier.detectMultiScale(
                    #     gray,
                    #     scaleFactor=scale_factor,
                    #     minNeighbors=min_neighbors,
                    #     minSize=tuple(min_size)
                    # )
                    # data = (int(datetime.utcnow().timestamp() * 1000),
                    #         {"sensor": "camera", "unit": "faces", "value": float(len(faces))}, "picam")
                    # collector.collect(data)
                    # for (x, y, w, h) in faces:
                    #     cv2.rectangle(frame, (x, y), (x + w, y + h),
                    #                   (0, 255, 0), 2)
                    # self.last_frame = frame
                    if self._stop:
                        break
        finally:
            elapsed = int(datetime.utcnow().timestamp() * 1000) - start
            logging.info("Ran for %d ms @ %d frames (%.2f fps)" % (elapsed, frames,frames / int(elapsed / 1000)))
