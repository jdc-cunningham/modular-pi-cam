#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch8
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
    #disp = LCD_1inch8.LCD_1inch8(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch8.LCD_1inch8()
    Lcd_ScanDir = LCD_1inch8.SCAN_DIR_DFT  #SCAN_DIR_DFT = D2U_L2R
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image)
    font18 = ImageFont.truetype("../Font/Font00.ttf",18) 

    logging.info("draw point")

    draw.rectangle((1, 1,2, 2), fill = "BLACK")
    draw.rectangle((1, 7,3,9), fill = "BLACK")
    draw.rectangle((1,14,4,17), fill = "BLACK")
    draw.rectangle((1,21,5,25), fill = "BLACK")

    logging.info("draw line")
    draw.line([(10, 5),(40,35)], fill = "RED",width = 1)
    draw.line([(10,35),(40, 5)], fill = "RED",width = 1)
    draw.line([(80,20),(110,20)], fill = "RED",width = 1)
    draw.line([(95, 5),(95,35)], fill = "RED",width = 1)

    logging.info("draw rectangle")
    draw.rectangle([(10,5),(40,35)],fill = "WHITE",outline="BLUE")
    draw.rectangle([(45,5),(75,35)],fill = "BLUE")

    logging.info("draw circle")
    draw.arc((80,5,110,35),0, 360, fill =(0,255,0))
    draw.ellipse((115,5,145,35), fill = (0,255,0))

    logging.info("draw text")
    Font1 = ImageFont.truetype("../Font/Font01.ttf",16)
    Font2 = ImageFont.truetype("../Font/Font01.ttf",20)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",25)

    
    draw.text((5, 40), 'Hello world', fill = "BLACK",font=Font1)
    draw.text((5, 60), 'WaveShare', fill = "RED",font=Font2)
    draw.text((5, 80), '1234567890', fill = "GREEN",font=Font1)
    text= u"微雪电子"
    draw.text((5, 100),text, fill = "BLUE",font=Font3)
    
    #im_r=image.rotate(90)
    disp.ShowImage(image)

    time.sleep(3)
    logging.info("show image")
    image = Image.open('../pic/LCD_1inch8.jpg')	
    im_r=image.rotate(0)
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