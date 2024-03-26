import os, time
import subprocess

from threading import Thread
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from PIL import Image

class Camera:
  def __init__(self, main):
    self.main = main
    self.display = main.display
    self.display_dimensions = self.display.dimensions
    self.manual_mode = False
    self.img_base_path = os.getcwd() + "/captured-media/"
    self.live_preview_active = False
    self.live_preview_start = 0
    self.live_preview_pause = False
    self.zoom_level = 1 # 1, 4 capped to 4 because 16x would be way too much (OLED refresh rate and vibration of hand)
    self.pan_offset_x = 0 # depends on zoom level, should be at center crop
    self.pan_offset_y = 0 # these are -2, -1, 0, 1, 2
    self.crop = [320, 320]
    self.last_mode = "small"
    self.timelapse_active = False
    self.has_autofocus = False # v3 modules have it
    self.max_resolution = [0, 0]
    self.scale_width = self.display_dimensions[0] # determined by display width and active zoom factor
    self.pan_offset_size = self.scale_width
    self.scale_width_4x = self.scale_width * 3
    self.scale_width_16x = self.scale_width * 5

    self.which_camera()

  def which_camera(self):
    cam_info = subprocess.check_output("libcamera-hello --list-cameras", shell=True)

    # ex
    '''
    Available cameras
    -----------------
    0 : imx477 [4056x3040 12-bit RGGB] (/base/soc/i2c0mux/i2c@1/imx477@1a)
            Modes: 'SRGGB10_CSI2P' : 1332990 [120.05 fps - (696, 528)/2664x1980 crop]
                   'SRGGB12_CSI2P' : 2028x1080 [50.03 fps - (0, 440)/4056x2160 crop]
                                     2028x1520 [40.01 fps - (0, 0)/4056x3040 crop]
                                     4056x3040 [10.00 fps - (0, 0)/4056x3040 crop]
    '''

    # HQ cam
    # https://stackoverflow.com/a/33054552/2710227
    if (b'imx477' in cam_info):
      self.resolution = '12.3 MP'
      self.name = 'HQ Cam'
      self.max_resolution = [4056, 3040]

    # v3 modules
    if (b'imx708_wide' in cam_info):
      self.resolution = '11.9 MP'
      self.camera_name = 'V3 Module Wide'
      self.max_resolution = [4608, 2592]

    if (b'imx708' in cam_info):
      self.resolution = '11.9 MP'
      self.name = 'V3 Module Standard'
      self.max_resolution = [4608, 2592]

    # v2
    if (b'imx219' in cam_info):
      self.resolution = '8 MP'
      self.name = 'V2 Module'
      self.max_resolution = [3280, 2464]

    # v1
    if (b'ov5647' in cam_info):
      self.resolution = '5 MP'
      self.name = 'V1 Module'
      self.max_resolution = [2592, 1944]

    self.setup()

  def setup(self):
    self.encoder = H264Encoder()
    self.picam2 = Picamera2()
    # writing this down here while fresh
    # depending on the display style, you may have to use a square image instead of rectangle and crop it
    # adds to dificulty of dynamic software
    self.config = self.picam2.create_still_configuration() # also same as 16x
    self.video_config = self.picam2.create_video_configuration()
    self.picam2.configure(self.config)
    self.start()

  def start(self):
    self.picam2.start()

  def stop(self):
    self.picam2.stop()
  
  def start_video_recording(self):
    video_filename =  self.img_base_path + str(time.time()).split(".")[0] + ".h264"
    self.picam2.start_recording(self.encoder, video_filename, quality=Quality.HIGH)

  def stop_video_recording(self):
    self.picam2.stop_recording()

  def change_mode(self, mode):
    if (mode == "full"):
      print('full')
      self.scale_width = self.display_dimensions[0]
    elif (mode == "zoom 4x"):
      print('zoom 4x')
      self.scale_width = self.scale_width_4x
    elif (mode == "16x"):
      print('zoom 16x')
      self.scale_width = self.scale_width_16x
    elif (mode == "video"):
      self.picam2.switch_mode(self.video_config)
    else:
      self.picam2.switch_mode(self.config)
    
    self.last_mode = mode
    self.crop = [self.scale_width, self.scale_width] # square

  # https://stackoverflow.com/a/451580/2710227
  def scale_image(self, img, new_width):
    base_width= new_width
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    return img

  # here you can crop/pan the image before it is displayed on the OLED
  def check_mod(self, pil_img_param):
    pil_img = self.scale_image(pil_img_param, self.scale_width)

    if (self.zoom_level > 1):
      return pil_img.crop((self.pan_offset[0], self.pan_offset[1], self.pan_offset[0] + self.crop[0], self.pan_offset[1] + self.crop[1]))
    else:
      return pil_img

  def live_preview(self):
    self.display.clear_screen()

    while (self.live_preview_active):
      branch_hit = False

      if (not self.live_preview_pause):
        branch_hit = True
        pil_img = self.picam2.capture_image()
        pil_img = self.check_mod(pil_img) # bad name
        self.display.show_image(pil_img, True)

      # after 1 min turn live preview off
      if (time.time() > self.live_preview_start + 60 and not self.live_preview_pause):
        branch_hit = True
        self.live_preview_pause = True
        self.zoom_level = 1
        self.pan_offset = [0, 0]
        self.scale_width = self.display_dimensions[0]
        self.display.clear_screen()
        self.change_mode("small")
        self.display.start_menu()

      if (not branch_hit):
        time.sleep(0.1)

      branch_hit = False

  def start_live_preview(self):
    Thread(target=self.live_preview).start()
    self.main.processing = False # this is everywhere... sucks

  def take_photo(self):
    img_path = self.img_base_path + str(time.time()).split(".")[0] + ".jpg"
    self.change_mode("full")
    self.picam2.capture_file(img_path)
    self.change_mode(self.last_mode)

  def timelapse(self):
    while (self.timelapse_active):
      time.sleep(300) # 5 minutes, in the future set by menu display, normally longer
      self.take_photo()

  def start_timelapse(self):
    self.change_mode("full")
    self.timelapse_active = True
    Thread(target=self.timelapse).start()

  def stop_timelapse(self):
    self.timelapse_active = False
    self.change_mode("small")

  def reset_preview_time(self):
    self.live_preview_start = time.time()

  def toggle_live_preview(self, pause):
    self.live_preview_pause = not pause # double negative dumb

  def set_live_preview_active(self, preview_active):
    if (preview_active):
      self.reset_preview_time()
      self.toggle_live_preview(True)
      self.live_preview_active = True
      self.main.live_preview_active = True
    else:
      # eg. in video mode
      self.live_preview_pause = True
      self.main.live_preview_active = False
      self.display.start_menu()

  def handle_shutter(self):
    self.reset_preview_time()

    # start live preview again
    if (self.live_preview_active and self.live_preview_pause):
      self.toggle_live_preview(True)
      self.main.processing = False
      return

    if (not self.live_preview_active):
      self.set_live_preview_active(True)
      self.start_live_preview()
    else:
      self.toggle_live_preview(False)
      time.sleep(0.3) # allow live_preview thread to pick this up/stop painting oled
      self.display.clear_screen()
      self.display.draw_text("Taking photo...")
      self.take_photo()
      self.display.clear_screen()
      self.display.draw_text("Photo captured")
      self.toggle_live_preview(True)
    
    self.main.processing = False

  def zoom_in(self):
    self.main.zoom_active = True

    if (self.zoom_level == 4):
      self.zoom_level = 16
      self.change_mode("zoom 16x")

    if (self.zoom_level == 1):
      self.zoom_level = 4
      self.change_mode("zoom 4x")

  def zoom_out(self):
    if (self.zoom_level == 4):
      self.zoom_level = 1
      self.change_mode("full")
      self.zoom_active = False
      self.main.zoom_active = False
    
    if (self.zoom_level == 16):
      self.zoom_level = 4
      self.change_mode("zoom 4x")

  def handle_zoom(self, button):
    self.reset_preview_time()

    if (button == "CENTER"):
      self.zoom_in()
    else:
      self.zoom_out()

    self.main.processing = False

  # the panning is based on the display dimension which is the result of full sensor size scaled down by PIL
  # cropped if necessary
  def handle_pan(self, button):
    self.reset_preview_time()

    # this may not be perfectly covering all surface area of the image
    if (button == "UP"):
      if (self.zoom_level == 4):
        if (self.pan_offset_y > -1):
          self.pan_offset_y -= 1
      if (self.zoom_level == 16):
        if (self.pan_offset_y > -2):
          self.pan_offset_y -= 1
    if (button == "DOWN"):
      if (self.zoom_level == 4):
        if (self.pan_offset_y < 1):
          self.pan_offset_y += 1
      if (self.zoom_level == 16):
        if (self.pan_offset_y < 2):
          self.pan_offset_y += 1
    if (button == "LEFT"):
      if (self.zoom_level == 4):
        if (self.pan_offset_x > -1):
          self.pan_offset_x -= 1
      if (self.zoom_level == 16):
        if (self.pan_offset_x > -2):
          self.pan_offset_x -= 1
    if (button == "RIGHT"):
      if (self.zoom_level == 4):
        if (self.pan_offset_x < 1):
          self.pan_offset_y += 1
      if (self.zoom_level == 16):
        if (self.pan_offset_y < 2):
          self.pan_offset_y += 1
    
    self.main.processing = False
