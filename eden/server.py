import cv2
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time


class FrameReader:

    def __init__(self, source):
        self.source = source

    def read(self):
        return (int(self.source.last_frame is not None), self.source.last_frame)


def get_handler(frame_reader):
    class CamHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            self.send_response(200)
            self.send_header(
                'Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc, img = frame_reader.read()
                    if not rc:
                        continue
                    ret, jpeg = cv2.imencode('.jpg', img)
                    jpeg = jpeg.tobytes()
                    self.wfile.write("--jpgboundary".encode("utf8"))
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(jpeg)))
                    self.end_headers()
                    self.wfile.write(jpeg)
                except:
                    break
    return CamHandler


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run_server(capture, host, port):
    server = None
    try:
        frame_reader = FrameReader(capture)
        server = ThreadedHTTPServer(
            (host, port), get_handler(frame_reader))
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if server:
            server.socket.close()
