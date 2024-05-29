import cv2
import os, time
import subprocess
import numpy as np

from threading import Thread
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import CircularOutput
from PIL import Image
from libcamera import controls

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
    self.zoom_level = 1
    self.pan_offset_x = 0 # based on block multiples eg. 3x = 3 blocks [0, 1, 2]
    self.pan_offset_y = 0
    self.crop = [320, 320]
    self.last_mode = "zoom 1x"
    self.timelapse_active = False
    self.has_autofocus = False # v3 modules have it
    self.max_resolution = [0, 0]
    self.recording_video = False
    self.recording_start = 0
    self.encoder = H264Encoder(30000000, repeat=True)
    self.encoder.output = CircularOutput(buffersize = 150)
    self.video_filename = ""
    self.video_processing = False

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
      self.main.v3_cam = True

    if (b'imx708' in cam_info):
      self.resolution = '11.9 MP'
      self.name = 'V3 Module Standard'
      self.max_resolution = [4608, 2592]
      self.main.v3_cam = True

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
    self.picam2 = Picamera2()
    # writing this down here while fresh
    # depending on the display style, you may have to use a square image instead of rectangle and crop it
    # adds to dificulty of dynamic software
    self.config = self.picam2.create_still_configuration(main={"size": self.picam2.sensor_resolution}, lores={"size": (320, 320)})
    self.config_1x = self.picam2.create_still_configuration(main={"size": (320, 320)}) # 320 is based on display size
    self.config_3x = self.picam2.create_still_configuration(main={"size": (960, 960)}) # x3 so a step in either direction
    self.config_7x = self.picam2.create_still_configuration(main={"size": (2240, 2240)}) # x7
    self.video_config = self.picam2.create_video_configuration(main={"size": (1920, 1080), "format":"RGB888"}, lores={"size": (400, 400), "format": "YUV420"})
    self.picam2.configure(self.config_1x)
    self.start()

  def start(self):
    self.picam2.start()

  def stop(self):
    self.picam2.stop()

  # https://forums.raspberrypi.com/viewtopic.php?t=366084#p2197540
  # https://github.com/raspberrypi/picamera2/blob/main/examples/yuv_to_rgb.py
  def sample_video(self, np_arr):
    rgb_img = cv2.cvtColor(np_arr, cv2.COLOR_YUV420p2RGB)
    rgb_img2 = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(np.uint8(rgb_img2))
    self.display.show_image(pil_img, "video")

  def record_video(self):
    video_file_path =  self.img_base_path + self.video_filename
    self.encoder.output.fileoutput = video_file_path
    self.encoder.output.start()

    while (self.recording_video):
      cap = self.picam2.capture_array("lores")
      self.sample_video(cap)
      time.sleep(0.03)

  def start_video_recording(self):
    # force 1 video at a time
    if (self.video_processing):
      self.main.display.draw_text("Video processing")
      time.sleep(2)
      self.main.active_menu = "Home"
      self.main.display.start_menu()
    else:
      self.video_processing = True
      self.video_filename = str(time.time()).split(".")[0] + ".h264"
      self.recording_video = True
      self.change_mode("video")
      self.recording_time = time.time()
      self.picam2.start_encoder(self.encoder)
      self.picam2.set_controls({"FrameRate": 30})

      # the mic is assumed to always be plugged in or not
      # since plugging it back in turns off the pi
      if (self.main.usb.mic_available):
        self.main.mic.record(self.img_base_path + self.video_filename)

      Thread(target=self.record_video).start()

  def stop_video_recording(self):
    if (self.main.mic != None):
      self.main.mic.recording = False

    self.recording_video = False
    self.recording_time = 0
    self.encoder.output.stop()
    self.picam2.stop_encoder()
    self.change_mode("zoom 1x")
    # this does block the menu from rendering immediately
    # depends how long the video is
    # can set it as another thread or don't do it

    if (self.main.mic == None):
      cmd = 'ffmpeg -framerate 30 -i ' + self.img_base_path + self.video_filename
      cmd += ' -c copy ' + self.img_base_path + self.video_filename + '.mp4'
      os.system(cmd)
      self.main.display.draw_text("Recording saved")
      self.video_processing = False
      time.sleep(2)
      self.main.active_menu = "Home"
      self.main.display.start_menu()

  def change_mode(self, mode):
    self.last_mode = mode

    if (mode == "zoom 1x"):
      self.zoom_level = 1
      self.pan_offset_x = 0
      self.pan_offset_y = 0
      self.picam2.switch_mode(self.config_1x)
      self.main.zoom_active = False
    elif (mode == "zoom 3x"):
      self.zoom_level = 3
      self.pan_offset_x = 1
      self.pan_offset_y = 1
      self.picam2.switch_mode(self.config_3x)
    elif (mode == "zoom 7x"):
      self.zoom_level = 7
      self.pan_offset_x = 3
      self.pan_offset_y = 3
      self.picam2.switch_mode(self.config_7x)
    elif (mode == "video"):
      self.picam2.switch_mode(self.video_config)
    else:
      self.picam2.switch_mode(self.config)
      self.last_mode = "zoom 1x" # reset

  # https://stackoverflow.com/a/451580/2710227
  def scale_image(self, img, new_width):
    base_width= new_width
    wpercent = (base_width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    return img

  # here you can crop/pan the image before it is displayed on the OLED
  def check_mod(self, pil_img):
    if (self.zoom_level > 1):
      tlx_offset = self.pan_offset_x * self.crop[0]
      tly_offset = self.pan_offset_y * self.crop[1]
      brx_offset = tlx_offset + self.crop[0]
      bry_offset = tly_offset + self.crop[1]
      # print('zoom lvl' + str(self.zoom_level))
      # print(str(tlx_offset), str(tly_offset), str(brx_offset), str(bry_offset))
      return pil_img.crop((tlx_offset, tly_offset, brx_offset, bry_offset))
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

        if (self.main.v3_cam):
          pil_img = self.display.stamp_img(pil_img)

        self.display.show_image(pil_img, True)

      # after 1 min turn live preview off
      if (time.time() > self.live_preview_start + 60 and not self.live_preview_pause):
        branch_hit = True
        self.live_preview_pause = True
        self.display.clear_screen()
        self.change_mode("zoom 1x")
        self.display.start_menu()

      if (not branch_hit):
        time.sleep(0.1)

      branch_hit = False

  def start_live_preview(self):
    Thread(target=self.live_preview).start()
    self.main.processing = False # this is everywhere... sucks

  def photo_saved(self, path):
    file_info = os.stat(path)

    return file_info.st_size > 0

  def take_photo(self):
    self.reset_preview_time()
    img_path = self.img_base_path + str(time.time()).split(".")[0] + ".jpg"
    self.change_mode("full")
    self.picam2.capture_file(img_path)
    time.sleep(0.15) # delay may help to save?
    self.change_mode(self.last_mode)

    return img_path

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
    self.change_mode("zoom 1x")

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
      photo_path = self.take_photo()
      self.display.clear_screen()

      if (self.photo_saved(photo_path)):
        self.display.draw_text("Photo captured")
      else:
        self.display.draw_text("Photo failed") # lol get rekt

      self.toggle_live_preview(True)
      time.sleep(0.3)
    
    self.main.processing = False

  def zoom_in(self):
    self.main.zoom_active = True

    if (self.zoom_level == 1):
      self.change_mode("zoom 3x")
      return

    if (self.zoom_level == 3):
      self.change_mode("zoom 7x")
      return

  def zoom_out(self):
    if (self.zoom_level == 7):
      self.change_mode("zoom 3x")
      return

    if (self.zoom_level == 3):
      self.change_mode("zoom 1x")

  def handle_zoom(self, button):
    self.reset_preview_time()

    if (button == "CENTER" and self.zoom_level < 7):
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
      if (self.zoom_level == 3):
        if (self.pan_offset_y > 0):
          self.pan_offset_y -= 1
      if (self.zoom_level == 7):
        if (self.pan_offset_y > 0):
          self.pan_offset_y -= 1

    if (button == "DOWN"):
      if (self.zoom_level == 3):
        if (self.pan_offset_y < 2):
          self.pan_offset_y += 1
      if (self.zoom_level == 7):
        if (self.pan_offset_y < 6):
          self.pan_offset_y += 1

    if (button == "LEFT"):
      if (self.zoom_level == 3):
        if (self.pan_offset_x > 0):
          self.pan_offset_x -= 1
      if (self.zoom_level == 7):
        if (self.pan_offset_x > 0):
          self.pan_offset_x -= 1

    if (button == "RIGHT"):
      if (self.zoom_level == 3):
        if (self.pan_offset_x < 2):
          self.pan_offset_x += 1
      if (self.zoom_level == 7):
        if (self.pan_offset_x < 6):
          self.pan_offset_x += 1
    
    self.main.processing = False

  def update_aperture(self):
    if (self.main.focus_level == -1):
      self.picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    else:
      # steps of 0.5 I guess, I'll use 1
      self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": self.main.focus_level})

    self.main.processing = False

  def handle_aperture(self, button):
    if (button == "UP"):
      if (self.main.focus_level < 10):
        self.main.focus_level += 1

    if (button == "DOWN"):
      if (self.main.focus_level > -1):
        self.main.focus_level -= 1

    self.update_aperture()

    
