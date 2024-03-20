# -*- coding:UTF-8 -*-

import io
import time
from picamera2 import Picamera2
from threading import Thread

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED

#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

#----------------------MAIN-------------------------#

def Display_Picture(File_Name):
  image = Image.open(File_Name)
  OLED.Display_Image(image)

try:
  def main():
    #-------------OLED Init------------#
    OLED.Device_Init()

    stop_camera = False
    get_photo = False
    photo = None

    def cam_thread(stop_camera, get_photo):
      global photo

      picam2 = Picamera2()
      config = picam2.create_still_configuration(main={"size": (128, 128)})
      picam2.configure(config)
      picam2.start()

      while (not stop_camera):
        if (get_photo):
          photo = picam2.capture_image()

    Thread(target=cam_thread, args=(stop_camera, get_photo)).start()

    while (True):
      print(photo)
      get_photo = True

      if (photo):
        get_photo = False
        OLED.Display_Buffer(photo.load())

      OLED.delay(60) # ms


  main()

# except Exception as e:
except:
    # print(e)
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()

