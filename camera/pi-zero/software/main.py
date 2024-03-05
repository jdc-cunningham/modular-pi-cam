# this code inspired by https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/main.py

import time

from display.display import Display
from buttons.buttons import Buttons
from camera.camera import Camera

class Main:
  def __init__(self):
    self.on = True
    self.processing = False
    self.display = Display()
    self.buttons = Buttons(self)
    self.camera = Camera(self)
    self.menu_pos = 0 # hardcoded for first version, doesn't belong here
    self.live_passthrough = False
    self.focus_level = -1 # -1 is auto, 0 is infinite, 1 is 1-3m, up to 10 which is 1/10 or 10cm
    self.live_preview_start = 0

    self.start_up()

    # keep main running
    while (self.on):
      # repaint menu particularly for battery
      if (self.menu_pos == 0):
        self.display.draw_menu("home")
      time.sleep(300)

  def start_up(self):
    self.buttons.start()

  def button_pressed(self, button):
    if (self.live_passthrough):
      self.live_preview_start = time.time()

      # set focus
      if (button == "UP"):
        if (self.focus_level < 10):
          self.focus_level += 1

      if (button == "DOWN"):
        if (self.focus_level > -1):
          self.focus_levle -= 1

    if (self.processing or self.live_passthrough):
      if (button == "SHUTTER"):
        self.camera.live_preview_pause = True
        self.camera.take_photo()
        self.camera.live_preview_pause = False
      return
    
    print("pressed " + button)

    if (button == "SHUTTER"):
      if (self.camera.live_preview_pause):
        self.live_passthrough = True
        self.camera.live_preview_pause = False
        self.camera.live_preview_start = time.time()
      else:
        self.live_passthrough = True
        self.camera.start()
        self.camera.live_preview_active = True
        self.camera.live_preview_start = time.time()
        self.camera.start_live_preview()

    if (button == "LEFT"):
      if (self.menu_pos == -1):
        self.menu_pos = 1
        self.display.draw_menu("settings")
        return

      if (self.menu_pos == 0): # you can make an array cycler just need to get it done right now
        self.menu_pos = -1
        self.display.draw_menu("files")
        return

      if (self.menu_pos == 1):
        self.menu_pos = 0
        self.display.draw_menu("home")
        return

    if (button == "RIGHT"):
      if (self.menu_pos == 1):
        self.menu_pos = -1
        self.display.draw_menu("files")
        return
      
      if (self.menu_pos == 0):
        self.menu_pos = 1
        self.display.draw_menu("settings")
        return

      if (self.menu_pos == -1):
        self.menu_pos = 0
        self.display.draw_menu("home")
        return
  
Main()
