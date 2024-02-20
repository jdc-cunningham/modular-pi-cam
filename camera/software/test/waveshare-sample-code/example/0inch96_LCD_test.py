#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_0inch96
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
    # disp = LCD_0inch96.LCD_0inch96(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_0inch96.LCD_0inch96()
    
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(100)
    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "BLUE")
    draw = ImageDraw.Draw(image1)
    
    Font1 = ImageFont.truetype("../Font/Font00.ttf",30)
    Font2 = ImageFont.truetype("../Font/Font00.ttf",12)
    Font3 = ImageFont.truetype("../Font/Font02.ttf",20)
    logging.info("draw text")
    draw.text((20, 0), u'微雪电子 ', font = Font1, fill = "WHITE")
    draw.text((1, 40), 'This is the LCD test program', font = Font2, fill = "BLACK")
    disp.ShowImage(image1)
    time.sleep(3)
    logging.info("draw line")
    
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
    draw.text((1, 40), u'Hellow WaveShare', font = Font2, fill = "BLACK")
    draw.text((70, 60), u'0123456789', font = Font2, fill = "RED")
    draw.text((00, 55), u'你好微雪', font = Font3, fill = "BLUE")
    disp.ShowImage(image2)
    time.sleep(3)
    
    logging.info("show image")
    image = Image.open('../pic/LCD_0inch96.jpg')	
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