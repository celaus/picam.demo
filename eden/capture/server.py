import cv2
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time


class FrameReader:

    def __init__(self, source):
        self.source = source

    def read(self):
        return (int(bool(source.last_frame)), source.last_frame)


def get_handler(frame_reader):
    class CamHandler(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path.endswith('.mjpg'):
                self.send_response(200)
                self.send_header(
                    'Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
                self.end_headers()
                while True:
                    try:
                        rc, img = frame_reader.read()
                        if not rc:
                            continue
                        ret, jpeg = cv2.imencode('.jpg', image)
                        self.wfile.write("--jpgboundary")
                        self.send_header('Content-type', 'image/jpeg')
                        self.send_header('Content-length', str(tmpFile.len))
                        self.end_headers()
                        self.wfile.write(jpeg.tobytes())
                        time.sleep(0.05)  # why?
                    except KeyboardInterrupt:
                        break
                return
            if self.path.endswith('.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("""
<html>
    <head></head>
    <body>
        <img src="/cam.mjpg"/>
    </body>
</html>""")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def run_server(capture, host, port):
    try:
        frame_reader = FrameReader(capture)
        server = ThreadedHTTPServer(
            (host, port), get_handler(frame_reader))
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.socket.close()
