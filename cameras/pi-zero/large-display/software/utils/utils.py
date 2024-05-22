import os, os.path, time, subprocess

from subprocess import run

class Utils:
  def __init__(self, main):
    self.main = main
    self.pi_ver = 1 # or 2 determine
    self.base_path = os.getcwd()
    self.capture_path = self.base_path + "/captured-media/"
    self.usb_path = None # maybe weird to be here

    self.get_pi_ver()

  # need this for OLED max SPI speed (refresh)
  # https://stackoverflow.com/a/72163326
  def get_pi_ver(self):
    # cmd = 'less "/proc/cpupinfo" | grep processor | wc -l' # was trying to use this initially
    cmd = 'less "/proc/cpuinfo" | grep processor'

    try:
      core_count = run(cmd, capture_output=True, shell=True, text=True)
      self.pi_ver = 2 if len(core_count.stdout.split("\n")) == 5 else 1 # this is dumb
    except:
      # I put this here because the above doesn't run on pi zero 1, 3.5.3 python
      print('failed to determine pi zero version')

  # https://stackoverflow.com/a/2632251
  def get_file_count(self):
    # -1 for gitkeep file
    return len([name for name in os.listdir(self.capture_path) if os.path.isfile(os.path.join(self.capture_path, name))]) - 1
  
  def get_files(self):
    files = os.listdir(self.capture_path)

    ret_files = []

    for file in files:
      if (not 'gitkeep' in file and not 'h264' in file):
        ret_files.append(file)

    return ret_files
  
  # https://stackoverflow.com/a/185941/2710227
  def delete_all_files(self):
    error_occurred = False

    self.main.display.render_deleting_files()

    for filename in os.listdir(self.capture_path):
      file_path = os.path.join(self.capture_path, filename)

      try:
        if ((os.path.isfile(file_path) or os.path.islink(file_path)) and '.gitkeep' not in file_path):
            os.unlink(file_path)
      except Exception as e:
          error_occurred = True
          print('Failed to delete %s. Reason: %s' % (file_path, e))

      time.sleep(0.05) # artificial delay

    msg = "Error Occurred" if error_occurred else "Files Deleted"

    self.main.display.render_deleting_files(msg)
    time.sleep(2)
    self.main.menu.update_state("BACK") # simulate back button event

  def get_usb_path(self):
    ignore_patterns = ['NAME', 'mmcblk', b'\xe2\x94\x94\xe2\x94\x80'.decode('utf-8')]

    dev_info = subprocess.check_output("lsblk", shell=True).splitlines()

    def check_ignore(name):
      for pat in ignore_patterns:
        if (pat in name):
          return True

      return False

    for line in dev_info:
      if (not check_ignore(line.decode('utf-8'))):
        self.usb_path = "/dev/" + line.decode('utf-8').split(' ')[0] + "1" # bad
        break

  # https://stackoverflow.com/a/39477913/2710227
  def mount_usb(self):
    try:
      self.get_usb_path()

      if (self.usb_path != None):
        if (not os.path.exists("/mnt/mpi-usb")):
          os.system("mkdir /mnt/mpi-usb")
        os.system("mount " + self.usb_path + " /mnt/mpi-usb")
    except Exception as e:
      print('failed to mount USB')
      return False
    
    return True
  
  def get_usb_details(self):
    usb_info = subprocess.check_output("df -h /mnt/mpi-usb", shell=True).splitlines()[1].decode('ascii')

    '''
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda1        30G  6.4M   30G   1% /mnt/mpi-usb
    '''

    usb_info_parts = usb_info.split(' ')
    
    incr = 0
    usb_size = None
    usb_used = None
    usb_avail = None
    usb_use = None

    for usb_info_part in usb_info_parts:
      if (incr == 0):
        incr += 1
        continue

      if (usb_size == None and usb_info_part != ''):
        usb_size = usb_info_part
        incr += 1
        continue

      if (usb_used == None and usb_info_part != ''):
        usb_used = usb_info_part
        incr += 1
        continue

      if (usb_avail == None and usb_info_part != ""):
        usb_avail = usb_info_part
        incr += 1
        continue

      if (usb_use == None and usb_info_part != ""):
        usb_use = usb_info_part
        break

      incr += 1

    return dict(
      size = usb_size,
      used = usb_used,
      avail = usb_avail,
      usage = usb_use
    )
  
  def get_files_to_transfer(self):
    files = []

    for filename in os.listdir(self.capture_path):
      file_path = os.path.join(self.capture_path, filename)

      if ('.gitkeep' not in file_path):
        files.append(dict(
          filename = filename,
          file = file_path,
          size_bytes = os.stat(file_path).st_size     
        ))

    return files
  
  def str_to_bytes(self, str_bytes):
    if ('m' in str_bytes):
      size = str_bytes.split('m')[0]
      return int(size) * 1000000

    # most likely
    if ('g' in str_bytes):
      size = str_bytes.split('g')[0]

    return int(size) * 1000000000

  def transfer_to_usb(self):
    if (self.mount_usb()):
      files = self.get_files_to_transfer()

      if (len(files) != 0):
        usb_info = self.get_usb_details()
        usb_avail = self.str_to_bytes(usb_info['avail'].lower())
        txfr_incr = 1

        for file in files:
          if (file['size_bytes'] < usb_avail):
            self.main.display.render_usb_transfer('Transferring ' + str(txfr_incr) + '/' + str(len(files)))
            os.system('cp ' + file['file'] + ' /mnt/mpi-usb/' + file['filename'])
            usb_avail = self.str_to_bytes(self.get_usb_details()['avail'].lower())
          else:
            self.main.display.render_usb_transfer('Not enough space')
            break

          txfr_incr += 1

        self.main.display.render_usb_transfer('Transfer complete')
        time.sleep(2)
        self.main.menu.update_state("BACK")
      else:
        self.main.display.render_usb_transfer('No files')
        