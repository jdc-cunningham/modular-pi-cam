# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

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
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # CENTER
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # BACK
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # SHUTTER

  def start(self):
    Thread(target=self.listen).start()

  # listen for input
  def listen(self):
    while True:
      if self.exit: return False

      if GPIO.input(4) == GPIO.HIGH:
        self.callback("UP")
      if GPIO.input(21) == GPIO.HIGH:
        self.callback("LEFT")
      if GPIO.input(18) == GPIO.HIGH:
        self.callback("CENTER")
      if GPIO.input(23) == GPIO.HIGH:
        self.callback("RIGHT")
      if GPIO.input(24) == GPIO.HIGH:
        self.callback("DOWN")
      if GPIO.input(26) == GPIO.HIGH:
        self.callback("BACK")
      if GPIO.input(12) == GPIO.HIGH:
        self.callback("SHUTTER")

      time.sleep(0.1)
