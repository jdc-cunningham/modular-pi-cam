#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch54
from PIL import Image,ImageDraw,ImageFont

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_1inch54.LCD_1inch54(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch54.LCD_1inch54()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)

    logging.info("draw point")

    draw.rectangle((5,10,6,11), fill = "BLACK")
    draw.rectangle((5,25,7,27), fill = "BLACK")
    draw.rectangle((5,40,8,43), fill = "BLACK")
    draw.rectangle((5,55,9,59), fill = "BLACK")

    logging.info("draw line")
    draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
    draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
    draw.line([(170,15),(170,55)], fill = "RED",width = 1)
    draw.line([(150,35),(190,35)], fill = "RED",width = 1)

    logging.info("draw rectangle")

    draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
    draw.rectangle([(85,10),(130,60)],fill = "BLUE")

    logging.info("draw circle")
    draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
    draw.ellipse((150,65,190,105), fill = (0,255,0))

    logging.info("draw text")
    Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",32)

    draw.rectangle([(0,65),(140,100)],fill = "WHITE")
    draw.text((5, 68), 'Hello world', fill = "BLACK",font=Font1)
    draw.rectangle([(0,115),(190,160)],fill = "RED")
    draw.text((5, 118), 'WaveShare', fill = "WHITE",font=Font2)
    draw.text((5, 160), '1234567890', fill = "GREEN",font=Font3)
    text= u"微雪电子"
    draw.text((5, 200),text, fill = "BLUE",font=Font3)
    im_r=image1.rotate(270)
    disp.ShowImage(im_r)
    time.sleep(3)
    logging.info("show image")
    image = Image.open('../pic/LCD_1inch54.jpg')	
    im_r=image.rotate(270)
    disp.ShowImage(im_r)
    time.sleep(3)
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()