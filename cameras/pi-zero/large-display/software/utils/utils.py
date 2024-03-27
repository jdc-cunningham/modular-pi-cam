import os, os.path

from subprocess import run

class Utils:
  def __init__(self):
    self.pi_ver = 1 # or 2 determine

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
    base_path = os.getcwd()
    capture_path = base_path + "/captured-media/"
    # -1 for gitkeep file
    return len([name for name in os.listdir(capture_path) if os.path.isfile(os.path.join(capture_path, name))]) - 1
  
  def get_files(self):
    base_path = os.getcwd()
    capture_path = base_path + "/captured-media/"
    files = os.listdir(capture_path)

    ret_files = []

    for file in files:
      if (not 'gitkeep' in file and not 'h264' in file):
        ret_files.append(file)

    return ret_files
