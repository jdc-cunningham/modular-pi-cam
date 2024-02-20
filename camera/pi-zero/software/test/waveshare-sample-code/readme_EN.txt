/*****************************************************************************
* | File      	:   Readme_EN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2020-06-17
* | Info        :   Here is an English version of the documentation for your quick use.
******************************************************************************/
This file is to help you use this routine.


1. Basic information:
This routine has been verified using the Separate LCD module. 
You can view the corresponding test routines in the \Examples\ of the project.
This Demo has been verified on the Raspberry Pi 4B;

2. Pin connection:
Pin connection You can view it in \lib\lcdconfig.py , and repeat it here:
EPD  	=>	RPI(BCM)
VCC    	->    	5V
GND    	->    	GND
DIN    	->    	10(SPI0_MOSI)
CLK    	->    	11(SPI0_SCK)
CS     	->    	8(CE0)
DC     	->    	25
RST    	->    	27
BL  	->    	18


3.Installation library
    sudo apt-get update
    sudo apt-get install python-pip
    sudo apt-get install python-pil
    sudo apt-get install python-numpy
    sudo pip install RPi.GPIO

or

    sudo apt-get update
    sudo apt-get install python3-pip
    sudo apt-get install python3-pil
    sudo apt-get install python3-numpy
    sudo pip3 install RPi.GPIO

4. Basic use:
Since this project is a comprehensive project, you may need to read the following for use:
You can view the test program in the examples\ directory.
Please note which LCD Module you purchased.
Chestnut 1:
     If you purchased 1.54inch LCD Module, then you should execute the command:
     Sudo python 1inch54_LCD_test.py