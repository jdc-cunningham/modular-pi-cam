# # https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
# this only accesses the 6050 (accel, gyro)
import smbus

from time import sleep
from threading import Thread

bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

# 6050 form factor which GY-91 has same shape
class Imu:
  def __init__(self):
    self.sample_imu = False # means its running
    self.accel = [0, 0, 0]
    self.gyro = [0, 0, 0]
    self.magnetometer = [0, 0, 0]
    self.barometer = 0 # lol, using GY-91, I guess you can tell if it's about to rain

  def read_raw_data(self, addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value
  
  def begin_sampling(self):
    self.sample_imu = True

    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

    while (self.sample_imu):
      #Read Accelerometer raw value
      acc_x = self.read_raw_data(ACCEL_XOUT_H)
      acc_y = self.read_raw_data(ACCEL_YOUT_H)
      acc_z = self.read_raw_data(ACCEL_ZOUT_H)
      
      #Read Gyroscope raw value
      gyro_x = self.read_raw_data(GYRO_XOUT_H)
      gyro_y = self.read_raw_data(GYRO_YOUT_H)
      gyro_z = self.read_raw_data(GYRO_ZOUT_H)
      
      #Full scale range +/- 250 degree/C as per sensitivity scale factor
      Ax = acc_x/16384.0
      Ay = acc_y/16384.0
      Az = acc_z/16384.0
      
      Gx = gyro_x/131.0
      Gy = gyro_y/131.0
      Gz = gyro_z/131.0
      
      self.accel = [Ax, Ay, Az]
      self.gyro = [Gx, Gy, Gz]

      sleep(0.167) # 60fps idk why

  def start(self):
    Thread(target=self.begin_sampling).start()