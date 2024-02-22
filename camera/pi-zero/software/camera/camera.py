import os, time

from threading import Thread
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

class Camera:
  def __init__(self, main):
    self.picam2 = Picamera2()
    self.encoder = H264Encoder()
