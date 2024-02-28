#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

# https://websockets.readthedocs.io/en/stable/intro/quickstart.html

import io
import logging
import socketserver
import os


from http import server
from threading import Condition, Thread
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from pathlib import Path

base_path = os.getcwd()

# build html page from parts since no static server

PAGE = ""

page_header = Path(base_path + "/videostream/web-ui/ui-header.html").read_text()
css_reset = Path(base_path + "/videostream/web-ui/css-reset.css").read_text()
css_style = Path(base_path + "/videostream/web-ui/styles.css").read_text()
page_header_2 = Path(base_path + "/videostream/web-ui/ui-header-2.html").read_text()
page_body = Path(base_path + "/videostream/web-ui/ui.html").read_text()
js_content = Path(base_path + "/videostream/web-ui/script.js").read_text()
page_body_2 = Path(base_path + "/videostream/web-ui/ui-2.html").read_text()

PAGE += page_header
PAGE += css_reset
PAGE += css_style
PAGE += page_header_2
PAGE += page_body
PAGE += js_content
PAGE += page_body_2

global_output = None

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == "/uxwing-line-angle-down-icon.svg":
            f = open(base_path + "/videostream/web-ui/uxwing-line-angle-down-icon.svg", 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(f.read())
        elif self.path == "/uxwing-line-angle-up-icon.svg":
            f = open(base_path + "/videostream/web-ui/uxwing-line-angle-up-icon.svg", 'rb')
            self.send_response(200)
            self.send_header('Content-Type', 'image/svg+xml')
            self.end_headers()
            self.wfile.write(f.read())
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with global_output.condition:
                        global_output.condition.wait()
                        frame = global_output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

picam2 = None
ExposureTime = int(0.004 * 1000000) # 1/250, microseconds
AnalogueGain = 1.0 # ISO 100

def start_video_stream():
    global picam2, global_output

    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.set_controls({"ExposureTime": ExposureTime, "AnalogueGain": AnalogueGain})
    global_output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(global_output))

    try:
        address = ('', 8000)
        global_output = global_output
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        picam2.stop_recording()

def stop():
    picam2.stop_recording()

def update_camera_values(which, value):
    global ExposureTime, AnalogueGain

    if (which == "shutter"):
        ExposureTime = int(float(value * 1000000))
        picam2.set_controls({"ExposureTime": ExposureTime, "AnalogueGain": AnalogueGain})

    if (which == "iso"):
        AnalogueGain = int(value)
        picam2.set_controls({"ExposureTime": ExposureTime, "AnalogueGain": AnalogueGain})