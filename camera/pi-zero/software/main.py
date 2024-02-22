# this code inspired by https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/main.py

import time

from buttons.buttons import Buttons
from display.display import Display

class Main:
  def __init__(self):
    self.processing = False
    self.display = None
    self.buttons = None

def button_pressed(self, button):
  if (self.processing):
      return
  
Main()
