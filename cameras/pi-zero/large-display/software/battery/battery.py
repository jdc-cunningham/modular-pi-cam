# https://github.com/jdc-cunningham/ml-hat-cam/blob/main/code/batt_db/batt_db.py

import sqlite3
import traceback
import time

from threading import Thread

# this is hardcoded since depending on what calls this file, the os.getcwd() output changes
base_path = "/home/pi/pi-zero-hq-cam/camera/software/"

class Battery:
  def __init__(self, main = None):
    self.con = sqlite3.connect(base_path + "/battery/battery.db", check_same_thread=False)
    self.init_batt_table()
    self.main = main

  def get_con(self):
    return self.con
  
  def get_cursor(self):
    return self.con.cursor()

  def init_batt_table(self):
    con = self.get_con()
    cur = self.get_cursor()
    table_exists = False

    try:
      table_exists = cur.execute("SELECT * FROM battery_status")
    except Exception:
      traceback.print_exc()
      table_exists = False

    if (not(table_exists)):
      try:
        # ids could be useful if switching batteries
        cur.execute("CREATE TABLE battery_status(uptime, max_uptime)") # minute units
        # 7.5 hrs soft cut off based on 18650 size of 3400mAh
        # need to run battery profiler to get better value
        cur.execute("INSERT INTO battery_status VALUES(?, ?)", [0, 450])
        con.commit()
      except Exception:
        print("create table error")
        traceback.print_exc()

  def get_uptime_info(self):
    cur = self.get_cursor()
    # this is dumb, but having issues where id column even non-rowid can't be found by CRON update call
    uptime = cur.execute("SELECT uptime, max_uptime FROM battery_status LIMIT 1")
    res = uptime.fetchone()

    if (res is None):
      return [0, 180] # disconnect with seed
    
    return res

  def update_batt_uptime(self, param_val = None):
    con = self.get_con()
    cur = self.get_cursor()
    prev_uptime = self.get_uptime_info()
    res = prev_uptime
    
    if (res is None):
      new_val = 5
    else:
      new_val = res[0] + 5

    cur.execute("UPDATE battery_status SET uptime = ? WHERE rowid = 1", [param_val or new_val])
    con.commit()

  def reset_uptime(self):
    con = self.get_con()
    cur = self.get_cursor()
    cur.execute("UPDATE battery_status SET uptime = ? WHERE rowid = 1", [0])
    con.commit()

  def get_remaining_capacity(self):
    uptime = self.get_uptime_info()

    if (uptime is None):
      return "100%"
    
    used_per = (uptime[0] / uptime[1]) * 100
    left_over = round(100 - used_per, 2)

    return left_over

  def get_batt_status(self):
    uptime = self.get_uptime_info()

    if (uptime is None):
      return "100%"
    
    used_per = (uptime[0] / uptime[1]) * 100
    left_over = round(100 - used_per, 2)

    return str(left_over) + "%"
  
  # determined from profiler/cron ticker
  def set_max_uptime(self, max_uptime_val = None):
    con = self.get_con()
    cur = self.get_cursor()
    uptime = self.get_uptime_info()
    max_uptime = max_uptime_val if max_uptime_val else uptime[0]
    cur.execute("UPDATE battery_status SET max_uptime = ? WHERE rowid = 1", [max_uptime])
    con.commit()
  
  def get_remaining_time(self):
    uptime = self.get_uptime_info()

    if (uptime is None):
      return "100%"
    
    left_over_mins = (uptime[1] - uptime[0])
    left_over_disp = ""

    if (left_over_mins < 60):
      left_over_disp = str(left_over_mins) + " mins"
    else:
      left_over_disp = str(round((left_over_mins / 60), 1)) + " hrs"

    return left_over_disp

  # this runs until the camera dies
  # depending on the size of your battery it could take several hours
  # you could reduce the down time for the OLED but I was concerned about burn in
  # should also make it look at some changing scene to help randomize what is displayed
  def profile_battery(self):
    while (self.run_profiler):
      # turn camera on every minute, it will turn the preview off after 1 minute
      self.main.camera.handle_shutter()
      time.sleep(125)
      uptime = self.get_uptime_info()
      prev_max_uptime = uptime[1]
      new_max_uptime = prev_max_uptime + 2 # minutes
      self.set_max_uptime(new_max_uptime)

  def start_profiler(self):
    self.reset_uptime()
    self.run_profiler = True
    time.sleep(3) # time to show message
    self.set_max_uptime(0) # reset to count upwards
    Thread(target=self.profile_battery).start()

  def stop_profiler(self):
    self.run_profiler = False
