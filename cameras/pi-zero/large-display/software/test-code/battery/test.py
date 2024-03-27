# https://stackoverflow.com/a/11096846
import sys
sys.path.append("../../")

from battery.battery import Battery

batt = Battery()

def dump_db_vals():
  print(batt.get_uptime_info())

def check_capacity():
  print(batt.get_remaining_capacity())

def set_max_uptime(val):
  batt.set_max_uptime(val)

# force question to show up on boot
set_max_uptime(5)
check_capacity()
dump_db_vals()