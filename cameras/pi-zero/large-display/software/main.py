'''
- boots
  - ask if charged (battery)
  - idle
    (click center button or shutter) show camera pass through, wait for buttons, maybe overlay telemetry/horizon,
  - shutter (photo)
  - non-center d-pad button (show/navigate menu)
  - CRON sqlite db counter for battery consumption
'''

import time

from buttons.buttons import Buttons
from battery.battery import Battery
from camera.camera import Camera
from menu.menu import Menu
from display.display import Display
from utils.utils import Utils
from usb.usb import Usb
from microphone.microphone import Microphone

class Main:
  def __init__(self):
    self.on = True
    self.display = None
    self.controls = None
    self.utils = None
    self.menu = None
    self.camera = None
    self.live_preview_active = False
    self.zoom_active = False
    self.processing = False # debouncer for button action
    self.active_menu = "Home"
    self.battery = None
    self.battery_needs_charge = False
    self.battery_profiler_active = False
    self.v3_cam = False
    self.focus_level = -1 # -1 is auto, 0 is infinite, 1 is 1-3m up to 10 which is 1/10 or 10cm 
    self.usb = None
    self.mic = None

    self.startup()

    # keep main running
    while (self.on):
      # repaint menu particularly for battery
      if (self.active_menu == "Home"):
        self.display.start_menu()
      time.sleep(300)

  def start_mic(self):
    self.mic = Microphone(self)

  # maybe shouldn't be here
  def check_battery(self):
    if (self.battery.get_remaining_capacity() <= 20):
      self.active_menu = "Battery Charged" # question lol
      self.display.render_battery_charged()
    else:
      self.display.start_menu()

  def startup(self):
    self.battery = Battery(self)
    self.utils = Utils(self)
    self.display = Display(self)
    self.camera = Camera(self)
    self.menu = Menu(self)
    self.display.show_boot_scene()
    self.controls = Buttons(self)
    self.usb = Usb(self)

    if (self.usb.mic_available):
      self.mic = Microphone(self)

    # self.camera.start() # moved to post camera check
    self.controls.start()
    self.check_battery()

  def button_pressed(self, button):
    # debouncer
    if (self.processing):
      return

    self.processing = True

    if (button == "SHUTTER"):
      if (self.active_menu == "Video"):
        self.menu.update_state(button)
      else:
        self.camera.handle_shutter()
    else:
      if (self.live_preview_active and button == "BACK"):
        if (self.zoom_active):
          self.camera.zoom_out()
        else:
          self.camera.toggle_live_preview(False)
          self.camera.live_preview_active = False
          self.live_preview_active = False
          time.sleep(0.15)
          self.display.start_menu()
        self.processing = False
      elif (self.live_preview_active and not self.zoom_active and self.v3_cam):
        self.camera.handle_aperture(button)
      elif (self.live_preview_active and (button == "CENTER" or button == "BACK")):
        self.camera.handle_zoom(button)
      elif (self.zoom_active and (button != "CENTER")):
        self.camera.handle_pan(button)
      elif (self.live_preview_active):
        self.processing = False
        return
      else:
        self.menu.update_state(button)

    # debounce
    time.sleep(0.3)

Main()
