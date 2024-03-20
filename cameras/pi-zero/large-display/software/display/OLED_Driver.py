 # -*- coding:UTF-8 -*-

# from:
# https://github.com/waveshare/1.5inch-RGB-OLED-Module/blob/master/python/OLED_Driver.py

import spidev

import RPi.GPIO as GPIO

import time

#SSD1351
SSD1351_WIDTH               = 128
SSD1351_HEIGHT              = 128
SSD1351_CMD_SETCOLUMN       = 0x15
SSD1351_CMD_SETROW          = 0x75
SSD1351_CMD_WRITERAM        = 0x5C
SSD1351_CMD_READRAM         = 0x5D
SSD1351_CMD_SETREMAP        = 0xA0
SSD1351_CMD_STARTLINE       = 0xA1
SSD1351_CMD_DISPLAYOFFSET   = 0xA2
SSD1351_CMD_DISPLAYALLOFF   = 0xA4
SSD1351_CMD_DISPLAYALLON    = 0xA5
SSD1351_CMD_NORMALDISPLAY   = 0xA6
SSD1351_CMD_INVERTDISPLAY   = 0xA7
SSD1351_CMD_FUNCTIONSELECT  = 0xAB
SSD1351_CMD_DISPLAYOFF      = 0xAE
SSD1351_CMD_DISPLAYON       = 0xAF
SSD1351_CMD_PRECHARGE       = 0xB1
SSD1351_CMD_DISPLAYENHANCE  = 0xB2
SSD1351_CMD_CLOCKDIV        = 0xB3
SSD1351_CMD_SETVSL          = 0xB4
SSD1351_CMD_SETGPIO         = 0xB5
SSD1351_CMD_PRECHARGE2      = 0xB6
SSD1351_CMD_SETGRAY         = 0xB8
SSD1351_CMD_USELUT          = 0xB9
SSD1351_CMD_PRECHARGELEVEL  = 0xBB
SSD1351_CMD_VCOMH           = 0xBE
SSD1351_CMD_CONTRASTABC     = 0xC1
SSD1351_CMD_CONTRASTMASTER  = 0xC7
SSD1351_CMD_MUXRATIO        = 0xCA
SSD1351_CMD_COMMANDLOCK     = 0xFD
SSD1351_CMD_HORIZSCROLL     = 0x96
SSD1351_CMD_STOPSCROLL      = 0x9E
SSD1351_CMD_STARTSCROLL     = 0x9F


#color
BLACK   = 0x0000
BLUE    = 0x001F
RED     = 0xF800
GREEN   = 0x07E0
CYAN    = 0x07FF
MAGENTA = 0xF81F
YELLOW  = 0xFFE0
WHITE   = 0xFFFF
#buffer
color_byte = [0x00, 0x00]
color_fill_byte = [0x00, 0x00]*(SSD1351_WIDTH)

#GPIO Set
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
OLED_RST_PIN = 27 # 25
OLED_DC_PIN  = 25 # 24
OLED_CS_PIN  = 8
GPIO.setup(OLED_RST_PIN, GPIO.OUT)
GPIO.setup(OLED_DC_PIN, GPIO.OUT)
GPIO.setup(OLED_CS_PIN, GPIO.OUT)
#GPIO init
GPIO.setwarnings(False)
GPIO.setup(OLED_RST_PIN, GPIO.OUT)
GPIO.setup(OLED_DC_PIN, GPIO.OUT)
GPIO.setup(OLED_CS_PIN, GPIO.OUT)
#SPI init
SPI = spidev.SpiDev(0, 0)
SPI.max_speed_hz = 9000000 # 21000000 if pi zero 2
SPI.mode = 0b00


def Set_Color(color):
    color_byte[0] = (color >> 8) & 0xff
    color_byte[1] = color & 0xff

def OLED_RST(x):
    if x == 1:
        GPIO.output(OLED_RST_PIN,GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_RST_PIN,GPIO.LOW)

def OLED_DC(x):
    if x == 1:
        GPIO.output(OLED_DC_PIN,GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_DC_PIN,GPIO.LOW)

def OLED_CS(x):
    if x == 1:
        GPIO.output(OLED_CS_PIN,GPIO.HIGH)
    elif x == 0:
        GPIO.output(OLED_CS_PIN,GPIO.LOW)

def SPI_WriteByte(byte):
    SPI.writebytes(byte)

def Write_Command(cmd):
    OLED_CS(0)
    OLED_DC(0)
    SPI_WriteByte([cmd])
    OLED_CS(1)

def Write_Data(dat):
    OLED_CS(0)
    OLED_DC(1)
    SPI_WriteByte([dat])
    OLED_CS(1)

def Write_Datas(data):
    OLED_CS(0)
    OLED_DC(1)
    SPI_WriteByte(data)
    OLED_CS(1)

def RAM_Address():
    Write_Command(0x15)
    Write_Data(0x00)
    Write_Data(0x7f)
    Write_Command(0x75)
    Write_Data(0x00)
    Write_Data(0x7f)

def Fill_Color(color):
    RAM_Address()
    Write_Command(0x5c)
    Set_Color(color)
    color_fill_byte = color_byte*SSD1351_WIDTH
    OLED_CS(0)
    OLED_DC(1)
    for i in range(0,SSD1351_HEIGHT):
        SPI_WriteByte(color_fill_byte)
    OLED_CS(1)

def Clear_Screen():
    RAM_Address()
    Write_Command(0x5c)
    color_fill_byte = [0x00, 0x00]*SSD1351_WIDTH
    OLED_CS(0)
    OLED_DC(1)
    for i in range(0,SSD1351_HEIGHT):
        SPI_WriteByte(color_fill_byte)
    OLED_CS(1)

def Draw_Pixel(x, y):
    # Bounds check.
    if ((x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT)):
        return
    if ((x < 0) or (y < 0)):
        return
    Set_Address(x, y)
    # transfer data
    Write_Datas(color_byte)

def Set_Coordinate(x, y):
    if((x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT)):
        return
    # Set x and y coordinate
    Write_Command(SSD1351_CMD_SETCOLUMN)
    Write_Data(x)
    Write_Data(SSD1351_WIDTH-1)
    Write_Command(SSD1351_CMD_SETROW)
    Write_Data(y)
    Write_Data(SSD1351_HEIGHT-1)
    Write_Command(SSD1351_CMD_WRITERAM)


def Set_Address(column, row):
    Write_Command(SSD1351_CMD_SETCOLUMN)  
    Write_Data(column)  #X start 
    Write_Data(column)  #X end 
    Write_Command(SSD1351_CMD_SETROW)
    Write_Data(row)     #Y start 
    Write_Data(row+7)   #Y end 
    Write_Command(SSD1351_CMD_WRITERAM) 

def Write_text(dat):
    for i in range(0,8):
        if(dat & 0x01):
            Write_Datas(color_byte)
        else:
            Write_Datas([0x00,0x00])
        dat = dat >> 1

def Invert(v):
    if(v):
        Write_Command(SSD1351_CMD_INVERTDISPLAY)
    else:
        Write_Command(SSD1351_CMD_NORMALDISPLAY)

def Draw_Pixel(x, y):
    # Bounds check.
    if((x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT)):
        return
    if((x < 0) or (y < 0)):
        return
    Set_Address(x, y)
    # transfer data
    Write_Datas(color_byte)

def Delay(x):
    time.sleep(x / 1000.0)
	
def Device_Init(pi_ver):
    global SPI

    if (pi_ver == 2):
        SPI.max_speed_hz = 21000000        

    OLED_CS(0)
    OLED_RST(0)
    Delay(500)
    OLED_RST(1)
    Delay(500)
    
    Write_Command(0xfd)	# command lock
    Write_Data(0x12)
    Write_Command(0xfd)	# command lock
    Write_Data(0xB1)
    
    Write_Command(0xae)	# display off
    Write_Command(0xa4)	# Normal Display mode
    
    Write_Command(0x15)	# set column address
    Write_Data(0x00)    # column address start 00
    Write_Data(0x7f)    # column address end 95
    Write_Command(0x75)	# set row address
    Write_Data(0x00)    # row address start 00
    Write_Data(0x7f)    # row address end 63	
    
    Write_Command(0xB3)
    Write_Data(0xF1)
    
    Write_Command(0xCA)
    Write_Data(0x7F)

    Write_Command(0xa0)	# set re-map & data format
    Write_Data(0x74)    # Horizontal address increment
    
    Write_Command(0xa1)	# set display start line
    Write_Data(0x00)    # start 00 line
    
    Write_Command(0xa2)	# set display offset
    Write_Data(0x00)
    
    Write_Command(0xAB)
    Write_Command(0x01)
    
    Write_Command(0xB4)
    Write_Data(0xA0)
    Write_Data(0xB5)
    Write_Data(0x55)
    
    Write_Command(0xC1)
    Write_Data(0xC8)
    Write_Data(0x80)
    Write_Data(0xC0)
    
    Write_Command(0xC7)
    Write_Data(0x0F)
    
    Write_Command(0xB1)
    Write_Data(0x32)
    
    Write_Command(0xB2)
    Write_Data(0xA4)
    Write_Data(0x00)
    Write_Data(0x00)
    
    Write_Command(0xBB)
    Write_Data(0x17)
    
    Write_Command(0xB6)
    Write_Data(0x01)
    
    Write_Command(0xBE)
    Write_Data(0x05)
    
    Write_Command(0xA6)
    
    Clear_Screen()
    Write_Command(0xaf)


# Draw a horizontal line ignoring any screen rotation.
def Draw_FastHLine(x, y, length):
    # Bounds check
    if((x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT)):
        return
    # X bounds check
    if((x+length) > SSD1351_WIDTH):
        length = SSD1351_WIDTH - x - 1
    if(length < 0):
        return
    # set location
    Write_Command(SSD1351_CMD_SETCOLUMN)
    Write_Data(x)
    Write_Data(x+length-1)
    Write_Command(SSD1351_CMD_SETROW)
    Write_Data(y)
    Write_Data(y)
    # fill!
    Write_Command(SSD1351_CMD_WRITERAM)
    
    for i in range(0,length):
        Write_Datas(color_byte)


def Draw_FastVLine(x, y, length):
    # Bounds check
    if((x >= SSD1351_WIDTH) or (y >= SSD1351_HEIGHT)):
        return
    # X bounds check
    if(y+length > SSD1351_HEIGHT):
        length = SSD1351_HEIGHT - y - 1
    if(length < 0):
        return
    # set location
    Write_Command(SSD1351_CMD_SETCOLUMN)
    Write_Data(x)
    Write_Data(x)
    Write_Command(SSD1351_CMD_SETROW)
    Write_Data(y)
    Write_Data(y+length-1)
    # fill!
    Write_Command(SSD1351_CMD_WRITERAM)

    for i in range(0,length):
        Write_Datas(color_byte)

def Display_Image(Image):
    if(Image == None):
        return
    
    Set_Coordinate(0,0)
    buffer1 = Image.load()
    for j in range(0, SSD1351_WIDTH):
        for i in range(0, SSD1351_HEIGHT):
            color_fill_byte[i*2] = ((buffer1[i,j][0] & 0xF8)|(buffer1[i,j][1] >> 5))
            color_fill_byte[i*2+1] = (((buffer1[i,j][1] << 3) & 0xE0)|(buffer1[i,j][2] >> 3))
        Write_Datas(color_fill_byte)

def Display_Buffer(Buffer):
    if(Buffer == None):
        return
    
    Set_Coordinate(0,0)
    buffer1 = Buffer
    for j in range(0, SSD1351_WIDTH):
        for i in range(0, SSD1351_HEIGHT):
            color_fill_byte[i*2] = ((buffer1[i,j][0] & 0xF8)|(buffer1[i,j][1] >> 5))
            color_fill_byte[i*2+1] = (((buffer1[i,j][1] << 3) & 0xE0)|(buffer1[i,j][2] >> 3))
        Write_Datas(color_fill_byte)