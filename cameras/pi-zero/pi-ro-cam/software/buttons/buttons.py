# https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/test-code/buttons/test_buttons.py

import RPi.GPIO as GPIO
import time

from threading import Thread

class Buttons():
  def __init__(self, main):
    self.exit = False
    self.callback = main.button_pressed

    # already set as BCM by OLED

    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # UP
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # LEFT
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # CENTER
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # SHUTTER

  def start(self):
    Thread(target=self.listen).start()

  # listen for input
  def listen(self):
    while True:
      if self.exit: return False

      # flip direction due to board being upside down
      if GPIO.input(4) == GPIO.HIGH: # UP
        self.callback("DOWN")
      if GPIO.input(21) == GPIO.HIGH: # LEFT
        self.callback("RIGHT")
      if GPIO.input(26) == GPIO.HIGH: # not used due to misfire other directions
        self.callback("CENTER")
      if GPIO.input(23) == GPIO.HIGH: # RIGHT
        self.callback("LEFT")
      if GPIO.input(24) == GPIO.HIGH: # DOWN
        self.callback("UP")
      if GPIO.input(12) == GPIO.HIGH:
        self.callback("SHUTTER")

      time.sleep(0.1)