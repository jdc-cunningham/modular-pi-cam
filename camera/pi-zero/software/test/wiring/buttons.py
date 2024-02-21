# https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/test-code/buttons/test_buttons.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # UP
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # LEFT
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # CENTER
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN\
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # SHUTTER

while True:
  if GPIO.input(4) == GPIO.HIGH:
    print("UP")
  if GPIO.input(21) == GPIO.HIGH:
    print("LEFT")
  if GPIO.input(18) == GPIO.HIGH:
    print("CENTER")
  if GPIO.input(23) == GPIO.HIGH:
    print("RIGHT")
  if GPIO.input(24) == GPIO.HIGH:
    print("DOWN")
  if GPIO.input(26) == GPIO.HIGH:
    print("BACK")
  if GPIO.input(12) == GPIO.HIGH:
    print("SHUTTER")

  time.sleep(0.05)