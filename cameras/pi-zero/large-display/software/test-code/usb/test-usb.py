import subprocess

ignore_patterns = ['mmcblk']

dev_info = subprocess.check_output("lsblk", shell=True).splitlines()

def check_ignore(name):
  for pat in ignore_patterns:
    if (pat in name):
      return True

  return False

for line in dev_info:
  print(check_ignore(line.decode('utf-8')))
  print(line.decode('utf-8').split(' ')[0])
