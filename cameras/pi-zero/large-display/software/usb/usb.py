import re, time, subprocess

from threading import Thread

class Usb:
  def __init__(self, main):
    self.main = main
    self.storage_available = False
    self.mic_available = False
    self.device_count = 0
    self.devices = []

    self.start()

  # https://stackoverflow.com/a/8265634/2710227
  def get_usb_devices(self):
    device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb")
    devices = []

    for i in df.split(b'\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
                devices.append(dinfo)

    return devices

  def scan_for_devices(self):
    while True:
      devices = self.get_usb_devices()

      if (self.device_count == 0):
         self.device_count = len(devices)
         self.devices = devices
      else:
        # change eg. mass storage plugged in
        # mic has to be plugged in before system starts due to power draw restarting GPU
        # https://forums.raspberrypi.com/viewtopic.php?t=237554
        if (self.device_count != len(devices)):
           print('new device')
           print(devices)
           self.device_count = len(devices)
           self.devices = devices

      time.sleep(0.5)

  def start(self):
     Thread(target=self.scan_for_devices).start()
