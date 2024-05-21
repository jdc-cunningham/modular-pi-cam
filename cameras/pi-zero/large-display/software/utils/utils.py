import os, os.path, time

from subprocess import run

class Utils:
  def __init__(self, main):
    self.main = main
    self.pi_ver = 1 # or 2 determine
    self.base_path = os.getcwd()
    self.capture_path = self.base_path + "/captured-media/"

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