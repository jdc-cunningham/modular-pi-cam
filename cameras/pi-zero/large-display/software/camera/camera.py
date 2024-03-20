import os, time

from threading import Thread
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality

class Camera:
  def __init__(self, main):
    self.main = main
    self.display = main.display
    self.manual_mode = False
    self.img_base_path = os.getcwd() + "/captured-media/"
    self.live_preview_active = False
    self.live_preview_start = 0
    self.live_preview_pause = False
    self.picam2 = Picamera2()
    self.encoder = H264Encoder()
    self.small_res_config = self.picam2.create_still_configuration(main={"size": (128, 128)}) # should not be a square
    self.zoom_4x_config = self.picam2.create_still_configuration(main={"size": (1014, 760)})
    self.full_res_config = self.picam2.create_still_configuration() # also same as 16x
    self.video_config = self.picam2.create_video_configuration()
    self.zoom_level = 1 # 1, 4 capped to 4 because 16x would be way too much (OLED refresh rate and vibration of hand)
    self.pan_offset = [0, 0] # depends on zoom level, should be at center crop
    self.crop = [128, 128]
    self.last_mode = "small"
    self.timelapse_active = False

    self.picam2.configure(self.small_res_config)

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
    if (mode == "full" or mode == "zoom 16x"):
      self.picam2.switch_mode(self.full_res_config)
    elif (mode == "zoom 4x"):
      self.picam2.switch_mode(self.zoom_4x_config)
      self.last_mode = mode
    elif (mode == "video"):
      self.picam2.switch_mode(self.video_config)
    else:
      self.picam2.switch_mode(self.small_res_config)
      self.last_mode = mode

  # here you can crop/pan the image before it is displayed on the OLED
  def check_mod(self, pil_img):
    if (self.zoom_level > 1):
      if (self.zoom_level == 4):
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
        self.display.display_buffer(pil_img.load())

      # after 1 min turn live preview off
      if (time.time() > self.live_preview_start + 60 and not self.live_preview_pause):
        branch_hit = True
        self.live_preview_pause = True
        self.zoom_level = 1
        self.pan_offset = [0, 0]
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

    if (self.zoom_level == 1):
      self.zoom_level = 4
      self.pan_offset = [443, 316] # based on (1014/2) - (128/2)
      self.change_mode("zoom 4x")

  def zoom_out(self):
    if (self.zoom_level == 4):
      self.zoom_level = 1
      self.change_mode("small")
      self.zoom_active = False
      self.main.zoom_active = False

  def handle_zoom(self, button):
    self.reset_preview_time()

    if (button == "CENTER"):
      self.zoom_in()
    else:
      self.zoom_out()

    self.main.processing = False

  # the panning is based on 128x128 divisions eg. 128/1014
  def handle_pan(self, button):
    self.reset_preview_time()

    # this may not be perfectly covering all surface area of the image
    if (button == "UP"):
      if (self.pan_offset[1] > 128):
        self.pan_offset[1] -= 128
      else:
        self.pan_offset[1] = 0
    if (button == "DOWN"):
      if (self.pan_offset[1] < 632):
        self.pan_offset[1] += 128
      else:
        self.pan_offset[1] = 632
    if (button == "LEFT"):
      if (self.pan_offset[0] > 128):
        self.pan_offset[0] -= 128
      else:
        self.pan_offset[0] = 128
    if (button == "RIGHT"):
      if (self.pan_offset[0] < 886):
        self.pan_offset[0] += 128
      else:
        self.pan_offset[0] = 886
    
    self.main.processing = False
