# https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/test-code/buttons/test_buttons.py

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # UP
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # LEFT
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # CENTER
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # SHUTTER

sample_count = 3
buttons_fired = []

def emit_btn_pressed():
  # dumb
  if (buttons_fired[0] == 'UP' and buttons_fired[1] == 'UP' and buttons_fired[2] == 'UP'):
    return 'UP'
  
  if (buttons_fired[0] == 'DOWN' and buttons_fired[1] == 'DOWN' and buttons_fired[2] == 'DOWN'):
    return 'DOWN'
  
  if (buttons_fired[0] == 'LEFT' and buttons_fired[1] == 'LEFT' and buttons_fired[2] == 'LEFT'):
    return 'LEFT'
  
  if (buttons_fired[0] == 'RIGHT' and buttons_fired[1] == 'RIGHT' and buttons_fired[2] == 'RIGHT'):
    return 'RIGHT'
  
  if (buttons_fired[0] == 'SHUTTER' and buttons_fired[1] == 'SHUTTER' and buttons_fired[2] == 'SHUTTER'):
    return 'SHUTTER'
  
  if ('CENTER' in buttons_fired):
    return 'CENTER'

def update_fired_btns(button_fired):
  if (len(buttons_fired) < sample_count):
    buttons_fired.append(button_fired)
    return emit_btn_pressed()
  else:
    buttons_fired.pop(0)

while True:
  if GPIO.input(4) == GPIO.HIGH:
    print("UP")
    update_fired_btns('UP')
  if GPIO.input(21) == GPIO.HIGH:
    print("LEFT")
    update_fired_btns('LEFT')
  if GPIO.input(26) == GPIO.HIGH:
    print("CENTER")
    update_fired_btns('CENTER')
  if GPIO.input(23) == GPIO.HIGH:
    print("RIGHT")
    update_fired_btns('RIGHT')
  if GPIO.input(24) == GPIO.HIGH:
    print("DOWN")
    update_fired_btns('DOWN')
  if GPIO.input(12) == GPIO.HIGH:
    print("SHUTTER")
    update_fired_btns('SHUTTER')

  time.sleep(0.05)
