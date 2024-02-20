#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch14
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
    #disp = LCD_1inch14.LCD_1inch14(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_1inch14.LCD_1inch14()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    
    # Create blank image for drawing.
    
    Font1 = ImageFont.truetype("../Font/Font00.ttf",30)
    Font2 = ImageFont.truetype("../Font/Font00.ttf",25)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",25)

    
    image2 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image2)
    
    logging.info("draw point")   
    draw.rectangle((1,1,2,2), fill = "BLACK")
    draw.rectangle((1,7,3,10), fill = "BLACK")
    draw.rectangle((1,13,4,17), fill = "BLACK")
    draw.rectangle((1,19,5,24), fill = "BLACK")
    
    logging.info("draw line")
    draw.line([(20, 1),(50, 31)], fill = "RED",width = 1)
    draw.line([(50, 1),(20, 31)], fill = "RED",width = 1)
    draw.line([(90,17),(122,17)], fill = "RED",width = 1)
    draw.line([(106,1),(106,33)], fill = "RED",width = 1)

    logging.info("draw rectangle")
    draw.rectangle([(20,1),(50,31)],fill = "WHITE",outline="BLUE")
    draw.rectangle([(55,1),(85,31)],fill = "BLUE")

    logging.info("draw circle")
    draw.arc((90,1,122,33),0, 360, fill =(0,255,0))
    draw.ellipse((125,1,158,33), fill = (0,255,0))
    
    logging.info("draw text")
    draw.text((1, 45), u'Hellow WaveShare', font = Font2, fill = "BLACK")
    draw.text((90, 82), u'0123456789', font = Font2, fill = "RED")
    draw.text((00, 85), u'你好微雪', font = Font3, fill = "BLUE")
    disp.ShowImage(image2)
    time.sleep(3)

    logging.info("show image")
    image = Image.open('../pic/LCD_1inch14.jpg')	
    disp.ShowImage(image)
    time.sleep(3)
    
    disp.module_exit()
    logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()
