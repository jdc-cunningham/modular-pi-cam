import os, os.path

base_path = "/home/pi/pi-zero-hq-cam/camera/software/"
capture_path = base_path + "/captured-media/"

print(os.listdir(capture_path))