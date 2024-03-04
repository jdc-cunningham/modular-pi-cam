# https://github.com/jdc-cunningham/pi-zero-hq-cam/blob/master/camera/software/camera/camera.py

import os, time

from threading import Thread
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from libcamera import controls

class Camera:
  def __init__(self, main):
    self.main = main
    self.display = main.display
    self.img_base_path = os.getcwd() + "/captured-media/"
    self.picam2 = Picamera2()
    self.encoder = H264Encoder()
    self.small_res_config = self.picam2.create_still_configuration(main={"size": (240, 240)}) # should not be a square
    self.full_res_config = self.picam2.create_still_configuration()
    self.last_mode = "small"
    self.live_preview_active = False
    self.live_preview_pause = False
    self.live_preview_start = 0

    self.picam2.configure(self.small_res_config)

  def start(self):
    self.picam2.start()
    # 0 is infinity, 1 is 1 meter. 10 max is closest 1/10 meters or 10 cm
    self.picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 0.0})

  def change_mode(self, mode):
    if (mode == "full"):
      self.picam2.switch_mode(self.full_res_config)
    else:
      self.picam2.switch_mode(self.small_res_config)
      self.last_mode = mode

  def take_photo(self):
    print('taking photo')
    img_path = self.img_base_path + str(time.time()).split(".")[0] + ".jpg"
    self.change_mode("full")
    self.picam2.capture_file(img_path)
    self.change_mode(self.last_mode)

  # you can do zoom-crop panning here
  def check_mod(self, pil_img):
    return pil_img
  
  def start_live_preview(self):
    Thread(target=self.live_preview).start()

  def live_preview(self):
    self.display.clear_screen()

    while (self.live_preview_active):
      branch_hit = False # wtf is this

      if (not self.live_preview_pause):
        branch_hit = True
        pil_img = self.picam2.capture_image()
        pil_img = self.check_mod(pil_img) # bad name
        pil_img_r = pil_img.rotate(270) # display is rotated left 90
        self.display.lcd.ShowImage(pil_img_r)

      # after 1 min turn live preview off
      if (time.time() > self.live_preview_start + 30 and not self.live_preview_pause):
        branch_hit = True
        self.main.live_passthrough = False
        self.live_preview_pause = True
        # self.zoom_level = 1
        # self.pan_offset = [0, 0]
        self.display.clear_screen()
        self.change_mode("small")
        self.display.draw_menu("home")

      if (not branch_hit):
        time.sleep(0.1)

      branch_hit = False