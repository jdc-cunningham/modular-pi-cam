# -*- coding:UTF-8 -*-

import io
import time
from picamera2 import Picamera2

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED

#--------------Image Library---------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

#-------------Test Display Functions---------------#

def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((0, 12), 'WaveShare', fill = "BLUE", font = font)
    draw.text((0, 36), 'Electronic', fill = "BLUE",font = font)
    draw.text((20, 72), '1.5 inch', fill = "CYAN", font = font)
    draw.text((10, 96), 'R', fill = "RED", font = font)
    draw.text((25, 96), 'G', fill = "GREEN", font = font)
    draw.text((40, 96), 'B', fill = "BLUE", font = font)
    draw.text((55, 96), ' OLED', fill = "CYAN", font = font)

    OLED.Display_Image(image)

def Draw_Text(text):
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((55, 96), ' OLED', fill = "WHITE", font = font)

    OLED.Display_Image(image)


def Test_Pattern():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.line([(0,8), (127,8)],   fill = "RED",    width = 16)
    draw.line([(0,24),(127,24)],  fill = "YELLOW", width = 16)
    draw.line([(0,40),(127,40)],  fill = "GREEN",  width = 16)
    draw.line([(0,56),(127,56)],  fill = "CYAN",   width = 16)
    draw.line([(0,72),(127,72)],  fill = "BLUE",   width = 16)
    draw.line([(0,88),(127,88)],  fill = "MAGENTA",width = 16)
    draw.line([(0,104),(127,104)],fill = "BLACK",  width = 16)
    draw.line([(0,120),(127,120)],fill = "WHITE",  width = 16)

    OLED.Display_Image(image)


def Test_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), ((OLED.SSD1351_WIDTH-1) - x, OLED.SSD1351_HEIGHT - 1)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, x)], fill = "RED", width = 1)
        draw.line([(0, 0), (OLED.SSD1351_WIDTH - 1, (OLED.SSD1351_HEIGHT-1) - x)], fill = "RED", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (x + int((OLED.SSD1351_WIDTH-1)/2), OLED.SSD1351_HEIGHT - 1)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x)], fill = "YELLOW", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, 0), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "YELLOW", width = 1)
        OLED.Display_Image(image)
    OLED.Delay(250)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x)], fill = "BLUE", width = 1)
        draw.line([(0, OLED.SSD1351_HEIGHT - 1), (OLED.SSD1351_WIDTH - 1, x + (OLED.SSD1351_HEIGHT-1)/2)], fill = "BLUE", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK", outline = "BLACK")
    OLED.Delay(250)

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x, 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (x + int((OLED.SSD1351_WIDTH-1)/2), 0)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x)], fill = "GREEN", width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1), (0, x + int((OLED.SSD1351_HEIGHT-1)/2))], fill = "GREEN", width = 1)
        OLED.Display_Image(image)
    draw.rectangle([0, 0, OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1], fill = "BLACK")


def Test_HV_Lines():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for y in range(0, OLED.SSD1351_HEIGHT - 1, 5):
        draw.line([(0, y), (OLED.SSD1351_WIDTH - 1, y)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)
    OLED.Delay(250)
    for x in range(0, OLED.SSD1351_WIDTH - 1, 5):
        draw.line([(x, 0), (x, OLED.SSD1351_HEIGHT - 1)], fill = "WHITE", width = 1)
    OLED.Display_Image(image)


def Test_Rects():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for x in range(0, int((OLED.SSD1351_WIDTH-1)/2), 6):
        draw.rectangle([(x, x), (OLED.SSD1351_WIDTH- 1 - x, OLED.SSD1351_HEIGHT-1 - x)], fill = None, outline = "WHITE")
    OLED.Display_Image(image)


def Test_FillRects(): 
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for x in range(OLED.SSD1351_HEIGHT-1, int((OLED.SSD1351_HEIGHT-1)/2), -6):
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = "BLUE", outline = "BLUE")
        draw.rectangle([(x, x), ((OLED.SSD1351_WIDTH-1) - x, (OLED.SSD1351_HEIGHT-1) - x)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)


def Test_Circles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    draw.ellipse([(0, 0), (OLED.SSD1351_WIDTH - 1, OLED.SSD1351_HEIGHT - 1)], fill = "BLUE", outline = "BLUE")
    OLED.Display_Image(image)
    OLED.Delay(500)
    for r in range(0, int(OLED.SSD1351_WIDTH/2) + 4, 4):
        draw.ellipse([(r, r), ((OLED.SSD1351_WIDTH-1) - r, (OLED.SSD1351_HEIGHT-1) - r)], fill = None, outline = "YELLOW")
    OLED.Display_Image(image)


def Test_Triangles():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)

    for i in range(0, int(OLED.SSD1351_WIDTH/2), 4):
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (255 - i*4, i*4, 255 - i*4), width = 1)
        draw.line([(i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i)], fill = (i*4, i*4 ,255 - i*4), width = 1)
        draw.line([(OLED.SSD1351_WIDTH - 1 - i, OLED.SSD1351_HEIGHT - 1 - i), (OLED.SSD1351_WIDTH/2, i)], fill = (i*4, 255 - i*4, i*4), width = 1)
        OLED.Display_Image(image)


def Display_Picture(File_Name):
    image = Image.open(File_Name)
    OLED.Display_Image(image)

#----------------------MAIN-------------------------#
try:

    def main():

        #-------------OLED Init------------#
        OLED.Device_Init()

        # try pi camera buffer
        # this is rancid, just testing

        picam2 = Picamera2()
        config = picam2.create_still_configuration(main={"size": (128, 128)})
        picam2.configure(config)
        picam2.start()

        while (True):
            pil_img = picam2.capture_image()
            OLED.Display_Buffer(pil_img.load())


    if __name__ == '__main__':
        main()

# except Exception as e:
except:
    # print(e)
    print("\r\nEnd")
    OLED.Clear_Screen()
    GPIO.cleanup()

