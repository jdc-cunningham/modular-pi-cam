import os
import time
import math

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
from .OLED_Driver import Device_Init, Display_Image, Clear_Screen, Display_Buffer

#--------------Image Library------------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

# temporary (lol)
from threading import Thread

#--------------Assets------------------#
base_path = os.getcwd() # root of repo eg. /software/ since main.py calls process

battery_sprite_path = base_path + "/menu/menu-sprites/battery_25_15.jpg"
folder_sprite_path = base_path + "/menu/menu-sprites/folder_21_18.jpg"
gear_sprite_path = base_path + "/menu/menu-sprites/gear_23_20.jpg"

small_font = ImageFont.truetype(base_path + "/display/alt-font.ttc", 13)
large_font = ImageFont.truetype(base_path + "/display/alt-font.ttc", 16)

class Display:
  def __init__(self, main):
    self.main = main
    self.active_img = None
    self.active_icon = None
    self.utils = main.utils
    self.file_count = self.utils.get_file_count() # maybe shouldn't be here

    # setup OLED
    Device_Init(main.utils.pi_ver)
  
  def render_menu_base(self, center_text = "Camera on", photo_text = "photo"):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((7, 3), photo_text, fill = "WHITE", font = small_font)
    draw.text((7, 105), "Auto", fill = "WHITE", font = small_font)
    # manual photography mode
    # draw.text((7, 90), "S: 1/60", fill = "WHITE", font = small_font)
    # draw.text((7, 105), "E: 100", fill = "WHITE", font = small_font)
    draw.text((22, 48), center_text, fill = "WHITE", font = large_font)
    draw.text((58, 3), self.main.battery.get_remaining_time(), fill = "WHITE", font = small_font)
    draw.text((60, 103), str(self.utils.get_file_count()), fill = "WHITE", font = small_font)

    battery_icon = Image.open(battery_sprite_path)
    folder_icon = Image.open(folder_sprite_path)
    gear_icon = Image.open(gear_sprite_path)

    image.paste(battery_icon, (98, 5))
    image.paste(folder_icon, (77, 103))
    image.paste(gear_icon, (101, 102))

    return image

  def start_menu(self):
    menu_base = self.render_menu_base()

    Display_Image(menu_base)

  def display_image(self, img_path):
    image = Image.open(img_path)
    Display_Image(image)

  def display_buffer(self, buffer):
    Display_Buffer(buffer)

  def clear_screen(self):
    Clear_Screen()

  def show_boot_scene(self):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    # look right
    draw.line([(20, 40), (50, 40)], fill = "WHITE", width = 3) # left eyebrow
    draw.line([(33, 44), (50, 44)], fill = "WHITE", width = 6) # left eye
    draw.line([(38, 48), (48, 48)], fill = "WHITE", width = 2) # left eye bottom

    draw.line([(75, 40), (105, 40)], fill = "WHITE", width = 3) # right eyebrow
    draw.line([(88, 44), (105, 44)], fill = "WHITE", width = 6) # right eye
    draw.line([(93, 48), (103, 48)], fill = "WHITE", width = 2) # right eye bottom

    draw.line([(40, 95), (35, 93)], fill = "WHITE", width = 1)  # mouth left
    draw.line([(40, 95), (90, 95)], fill = "WHITE", width = 1)  # mouth

    Display_Image(image)

    time.sleep(1)

    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    # wink
    draw.line([(20, 45), (50, 45)], fill = "WHITE", width = 3) # left eyebrow

    draw.line([(75, 40), (105, 40)], fill = "WHITE", width = 3) # right eyebrow
    draw.line([(88, 44), (105, 44)], fill = "WHITE", width = 6) # right eye
    draw.line([(93, 48), (103, 48)], fill = "WHITE", width = 2) # right eye bottom

    draw.line([(40, 95), (35, 93)], fill = "WHITE", width = 1)  # mouth left
    draw.line([(40, 95), (90, 95)], fill = "WHITE", width = 1)  # mouth

    Display_Image(image)

    time.sleep(0.5)

    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    # look right
    draw.line([(20, 40), (50, 40)], fill = "WHITE", width = 4)  # left eyebrow
    draw.line([(35, 45), (50, 45)], fill = "WHITE", width = 5)  # left eye
    draw.line([(38, 48), (48, 48)], fill = "WHITE", width = 2)  # left eye bottom

    draw.line([(75, 40), (105, 40)], fill = "WHITE", width = 4) # right eyebrow
    draw.line([(90, 45), (105, 45)], fill = "WHITE", width = 5) # right eye
    draw.line([(93, 48), (103, 48)], fill = "WHITE", width = 2) # right eye bottom

    draw.line([(40, 95), (35, 93)], fill = "WHITE", width = 1)  # mouth left
    draw.line([(40, 95), (90, 95)], fill = "WHITE", width = 1)  # mouth

    Display_Image(image)

    time.sleep(1)

    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((20, 55), "Pi Zero Cam", fill = "WHITE", font = large_font)
    draw.text((20, 70), "v 1.1.0", fill = "WHITE", font = small_font)

    Display_Image(image)

    time.sleep(3)

    self.clear_screen()

  def set_menu_center_text(self, draw, text, x = 22, y = 48):
    draw.text((x, y), text, fill = "WHITE", font = large_font)

  def draw_active_icon(self, icon_name):
    image = self.render_menu_base("")
    draw = ImageDraw.Draw(image)

    if (icon_name == "Files"):
      draw.line([(60, 121), (98, 121)], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Files")

    if (icon_name == "Camera Settings"):
      draw.line([(7, 121), (34, 121)], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Camera Settings", 5)

    if (icon_name == "Photo Video Toggle"):
      draw.line([(7, 22), (34, 22)], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Toggle Mode")

    if (icon_name == "Settings"):
      draw.line([(101, 122), (124, 122)], fill = "MAGENTA", width = 2)
      self.set_menu_center_text(draw, "Settings")
    
    Display_Image(image)
  
  def toggle_text(self, mode):
    if (mode == "video"):
      image = self.render_menu_base("Tap to record", "video")
    else:
      image = self.render_menu_base("Toggle Mode", "photo")

    Display_Image(image)

  def draw_text(self, text):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)
    font = large_font

    draw.text((0, 96), text, fill = "WHITE", font = font)

    Display_Image(image)

  def get_settings_img(self):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.line([(0, 0), (128, 0)], fill = "WHITE", width = 40)
    draw.text((5, 0), "Settings", fill = "BLACK", font = large_font)
    draw.text((5, 26), "Telemetry", fill = "WHITE", font = large_font)
    draw.text((5, 52), "Battery Profiler", fill = "WHITE", font = large_font)
    draw.text((5, 78), "Timelapse", fill = "WHITE", font = large_font)

    return image
  
  def render_settings(self):
    image = self.get_settings_img()

    Display_Image(image)

  def render_battery_profiler(self):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((0, 48), "Profiling battery", fill = "WHITE", font = large_font)
    draw.text((0, 72), "Press back to cancel", fill = "WHITE", font = small_font)

    Display_Image(image)

  def render_timelapse(self):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((0, 48), "5 min timelapse", fill = "WHITE", font = large_font)
    draw.text((0, 72), "Press back to cancel", fill = "WHITE", font = small_font)

    Display_Image(image)

  def render_battery_charged(self, is_charged = False):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.text((22, 48), "Battery Charged?", fill = "WHITE", font = small_font)
    draw.text((22, 72), "Yes", fill = "CYAN" if is_charged else "WHITE", font = small_font)
    draw.text((60, 72), "No", fill = "WHITE" if is_charged else "CYAN", font = small_font) # default option

    Display_Image(image)

  def draw_active_telemetry(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, 26), (0, 42)], fill = "MAGENTA", width = 2)

    Display_Image(image)

  def draw_active_battery_profiler(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, 52), (0, 68)], fill = "MAGENTA", width = 2)

    Display_Image(image)

  def draw_active_timelapse(self):
    image = self.get_settings_img()
    draw = ImageDraw.Draw(image)

    draw.line([(0, 78), (0, 94)], fill = "MAGENTA", width = 2)

    Display_Image(image)

  def render_live_telemetry(self):
    while (self.main.menu.active_menu_item == "Telemetry"):
      image = Image.new("RGB", (128, 128), "BLACK")
      draw = ImageDraw.Draw(image)

      accel = self.main.imu.accel
      gyro = self.main.imu.gyro

      draw.line([(0, 0), (128, 0)], fill = "WHITE", width = 40)
      draw.text((5, 0), "Raw Telemetry", fill = "BLACK", font = large_font)
      draw.text((5, 26), "accel x: " + str(accel[0])[0:8], fill = "WHITE", font = small_font)
      draw.text((5, 36), "accel y: " + str(accel[1])[0:8], fill = "WHITE", font = small_font)
      draw.text((5, 46), "accel z: " + str(accel[2])[0:8], fill = "WHITE", font = small_font)
      draw.text((5, 56), "gyro x: " + str(gyro[0])[0:8], fill = "WHITE", font = small_font)
      draw.text((5, 66), "gyro y: " + str(gyro[1])[0:8], fill = "WHITE", font = small_font)
      draw.text((5, 76), "gyro z: " + str(gyro[2])[0:8], fill = "WHITE", font = small_font)

      Display_Image(image)
    
  # special page, it is not static
  # has active loop to display data
  def render_telemetry_page(self):
    # this is not good, brought in main context into display to pull imu values
    Thread(target=self.render_live_telemetry).start()
  
  # this will need a background process to generate thumbnails
  # since it takes 5+ seconds to do the step below/show files

  # this takes a list of img file paths (up to 4)
  # if it's a video, need ffmpeg to get a thumbnail (future)
  # render the OLED scene with these images and pagination footer
  # yeah this is hard, need offsets
  # https://stackoverflow.com/a/451580
  def get_files_scene(self, file_paths, page, pages):
    image = Image.new("RGB", (128, 128), "BLACK")
    draw = ImageDraw.Draw(image)
    base_img_path = base_path + "/captured-media/"

    # this is dumb, my brain is blocked right now, panicking, too much to do
    # this code has to be reworked anyway this is like a demo
    page_map = [[], [0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11]] # matches file list

    new_size = (45, 45)

    files = page_map[page]
    
    for file in files:
      cam_image = Image.open(base_img_path + file_paths[file])
      base_width= 45
      wpercent = (base_width / float(cam_image.size[0]))
      hsize = int((float(cam_image.size[1]) * float(wpercent)))
      cam_image = cam_image.resize((base_width, hsize), resample=Image.LANCZOS)

      # this is dumb
      if (file == 0):
        image.paste(cam_image, (15, 7))
      if (file == 1):
        image.paste(cam_image, (67, 7))
      if (file == 2):
        image.paste(cam_image, (15, 60))
      if (file == 3):
        image.paste(cam_image, (67, 60))

    if (page > 1):
      draw.text((7, 110), "<", fill = "WHITE", font = small_font)

    draw.text((50, 110), str(page) + "/" + str(pages), fill = "WHITE", font = small_font)

    if (pages > 1):
      draw.text((110, 110), ">", fill = "WHITE", font = small_font)

    return image

  def render_files(self):
    files = self.utils.get_files()
    file_count = len(files)
    self.main.menu.files_pages = 1 if ((file_count / 4) < 1) else math.ceil(file_count / 4)

    if (file_count == 0):
      self.draw_text("No Files")
    else:
      self.main.active_menu = "Files"
      files_scene = self.get_files_scene(files, self.main.menu.files_page, self.main.menu.files_pages)
      Display_Image(files_scene)
