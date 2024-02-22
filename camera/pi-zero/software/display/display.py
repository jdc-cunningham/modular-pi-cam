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

# img paths
camera_sprite_path = "../menu/sprites/camera_120_89.png"
folder_sprite_path = "../menu/sprites/folder_120_96.png"
settings_sprite_path = "../menu/sprites/settings_120_120.png"
film_sprite_path = "../menu/sprites/film_120_131.png"

class Display:
  def __init__(self):
      self.lcd = LCD_1inch28.LCD_1inch28()
      # Initialize library.
      self.lcd.Init()

  def clear(self):
     self.lcd.clear()

  # proportional resize
  def resize_img(img, width):
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((width, hsize), resample=Image.LANCZOS)

  def draw_menu(self, which):
     if (which == 'home'):
      image = Image.open('../menu/sprites/base-blue-gradient.png')

      camera_icon = Image.open(camera_sprite_path)
      folder_sprite = Image.open(folder_sprite_path)
      settings_sprite = Image.open(settings_sprite_path)
      film_sprite = Image.open(film_sprite_path)

      # scale down side images
      folder_sprite_sm = self.resize_img(folder_sprite, 60)
      settings_sprite_sm = self.resize_img(settings_sprite, 60)

      image.paste(folder_sprite_sm, (30, 90))
      image.paste(camera_icon, (60, 60)) # middle of screen
      image.paste(settings_sprite_sm, (210, 90))

      # draw.text((40, 50), 'WaveShare', fill = (128,255,128), font=Font3)

      im_r = image.rotate(90)
      self.lcd.ShowImage(im_r)

Display()