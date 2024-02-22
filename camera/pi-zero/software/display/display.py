# based on Waveshare example code for 1inch28_LCD

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys 
import time
import logging
import spidev as SPI

sys.path.append("..")

from lib import LCD_1inch28
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)

Font3 = ImageFont.truetype("./Font/Font02.ttf",32) # normal

class Display:
  def __init__(self):
      disp = LCD_1inch28.LCD_1inch28()
      # Initialize library.
      disp.Init()

      # time.sleep(3)

      # Clear display.
      disp.clear()

      # Create blank image for drawing.
      # image1 = Image.new("RGB", (disp.width, disp.height), "BLACK")
      # draw = ImageDraw.Draw(image1)

      # draw.text((40, 50), 'WaveShare', fill = (128,255,128), font=Font3)

      # disp.ShowImage(image1)

      image = Image.open('../menu/sprites/base-blue-gradient.png')	
      im_r = image.rotate(180)
      disp.ShowImage(im_r)

      time.sleep(3)

      disp.clear()

Display()