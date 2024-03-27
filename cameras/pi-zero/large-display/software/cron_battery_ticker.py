# this is ran by CRON every 5 minutes to increment the battery uptime
# it counts towards the max_uptime which means 100% usage is 0 capacity, recharge
# shouldn't let it get that high that's absolutely exhausted where battery protection
# will be set to post a warning at 80% or more capacity

from battery.battery import Battery

batt = Battery()
batt.update_batt_uptime()