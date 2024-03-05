# based on Waveshare example code for 1inch28_LCD

#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys 
import time
import logging
import spidev as SPI

software_path = os.getcwd()

sys.path.append(software_path + "/display/")

from lib import LCD_1inch28
from PIL import Image, ImageDraw, ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 

# logging.basicConfig(level=logging.DEBUG) # noisy

Font3 = ImageFont.truetype(software_path + "/display/Font/Font02.ttf",32) # normal

# img paths
camera_sprite_path = software_path + "/menu/sprites/camera_120_89.png"
folder_sprite_path = software_path + "/menu/sprites/folder_120_96.png"
settings_sprite_path = software_path + "/menu/sprites/settings_120_120.png"
film_sprite_path = software_path + "/menu/sprites/film_120_131.png"

class Display:
  def __init__(self):
    self.lcd = LCD_1inch28.LCD_1inch28()

    self.lcd.Init()

    self.draw_menu("home")

  def clear(self):
    self.lcd.clear()

  def clear_screen(self):
    self.clear()

  def add_focus_level(self, live_preview_img, focus_level):
    draw = ImageDraw.Draw(live_preview_img)

    focus_text = 'AF' if focus_level == -1 else str('F ' + focus_level)

    draw.text((79, 180), focus_text, fill = (255,255,255), font=Font3)

    return draw

  # proportional resize
  def resize_img(self, img, width):
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    new_img = img.resize((width, hsize), resample=Image.LANCZOS)
    return new_img

  # hardcoded for now to get it done
  def draw_menu(self, which):
    if (which == 'home'):
      image = Image.open(software_path + '/menu/sprites/base-orange-solid.png')

      camera_icon = Image.open(camera_sprite_path)
      folder_sprite = Image.open(folder_sprite_path)
      settings_sprite = Image.open(settings_sprite_path)
      film_sprite = Image.open(film_sprite_path)

      # scale down side images
      folder_sprite_sm = self.resize_img(folder_sprite, 60)
      settings_sprite_sm = self.resize_img(settings_sprite, 60)

      image.paste(folder_sprite_sm, (-30, 90), mask=folder_sprite_sm) # 3rd param fixes transparency issue
      image.paste(camera_icon, (60, 75), mask=camera_icon) # middle of screen
      image.paste(settings_sprite_sm, (210, 90), mask=settings_sprite_sm)

      draw = ImageDraw.Draw(image)
      draw.text((79, 180), 'camera', fill = (0,0,0), font=Font3)

      im_r = image.rotate(90)
      self.lcd.ShowImage(im_r)

    if (which == 'files'): # left
      image = Image.open(software_path + '/menu/sprites/base-orange-solid.png')

      camera_icon = Image.open(camera_sprite_path)
      folder_sprite = Image.open(folder_sprite_path)
      settings_sprite = Image.open(settings_sprite_path)
      film_sprite = Image.open(film_sprite_path)

      # scale down side images
      camera_sprite_sm = self.resize_img(camera_icon, 60)
      settings_sprite_sm = self.resize_img(settings_sprite, 60)
      folder_sprite_sm = self.resize_img(folder_sprite, 60)

      image.paste(settings_sprite_sm, (-30, 90), mask=settings_sprite_sm) # 3rd param fixes transparency issue
      image.paste(folder_sprite, (60, 75), mask=folder_sprite) # middle of screen
      image.paste(camera_sprite_sm, (210, 90), mask=camera_sprite_sm)

      draw = ImageDraw.Draw(image)
      draw.text((79, 180), 'files', fill = (0,0,0), font=Font3)

      im_r = image.rotate(90)
      self.lcd.ShowImage(im_r)

    if (which == 'settings'): # right
      image = Image.open(software_path + '/menu/sprites/base-orange-solid.png')

      camera_icon = Image.open(camera_sprite_path)
      folder_sprite = Image.open(folder_sprite_path)
      settings_sprite = Image.open(settings_sprite_path)
      film_sprite = Image.open(film_sprite_path)

      # scale down side images
      camera_sprite_sm = self.resize_img(camera_icon, 60)
      folder_sprite_sm = self.resize_img(folder_sprite, 60)

      image.paste(camera_sprite_sm, (-30, 90), mask=camera_sprite_sm) # 3rd param fixes transparency issue
      image.paste(settings_sprite, (60, 60), mask=settings_sprite) # middle of screen
      image.paste(folder_sprite_sm, (210, 90), mask=folder_sprite_sm)

      draw = ImageDraw.Draw(image)
      draw.text((79, 180), 'settings', fill = (0,0,0), font=Font3)

      im_r = image.rotate(90)
      self.lcd.ShowImage(im_r)