import time

class Menu:
  def __init__(self, main):
    self.main = main
    self.display = main.display
    self.camera = main.camera
    self.menu_mode = True # or False for camera
    self.active_menu_item = None
    self.menu_x = 0 # -1, 0, 1
    self.menu_y = 0 # -2, -1, 0, 1 (-2 is towards top)
    self.menu_settings_y = 1 # I'm seeing the pattern now, grouping
    self.files_page = 1 # this shouldn't be here
    self.files_pages = 1
    self.files_y = 0 # footer or files
    self.recording_video = False
    self.battery_charged = False # yes, no question
    self.menu_daf_x = 1 # delete all files

  def update_state(self, button_pressed):
    if (self.main.active_menu == "Home"):
      if (button_pressed == "LEFT" and self.menu_x > -1):
        self.menu_x -= 1

      if (button_pressed == "RIGHT" and self.menu_x < 1):
        self.menu_x += 1
      
      if (button_pressed == "UP" and self.menu_y > -2):
        self.menu_y -= 1

      if (button_pressed == "DOWN" and self.menu_y < 1):
        self.menu_y += 1
    elif (self.main.active_menu == "Settings"):
      if (button_pressed == "DOWN" and self.menu_settings_y < 6):
        self.menu_settings_y += 1
      
      if (button_pressed == "UP" and self.menu_settings_y > 1):
        self.menu_settings_y -= 1

      if (button_pressed == "BACK"):
        if (self.active_menu_item == "Battery Profiler"):
          self.main.battery.stop_profiler()
        
        if (self.active_menu_item == "Delete All Files"):
          self.active_menu_item = None

        self.active_menu_item = None
        self.menu_settings_y = 0
        self.display.start_menu()
        self.main.active_menu = "Home"

      if (button_pressed == "CENTER"):
        if (self.active_menu_item == "Telemetry"):
          self.display.render_telemetry_page()
    
        if (self.active_menu_item == "Battery Profiler"):
          self.display.render_battery_profiler()
          self.main.battery.start_profiler()
          self.main.battery_profiler_active = True
        
        if (self.active_menu_item == "Reset Battery"):
          self.main.battery.reset_uptime()
      
        if (self.active_menu_item == "Timelapse"):
          self.main.active_menu = "Timelapse"
          self.display.render_timelapse()
          self.main.camera.start_timelapse()

        if (self.active_menu_item == "Delete All Files"):
          self.main.active_menu = "Delete All Files"
          self.display.render_delete_all_files()
    elif (self.main.active_menu == "Delete All Files"):
      if (button_pressed == "BACK"):
        self.main.active_menu = "Settings"
        self.display.render_settings()

      if (button_pressed == "LEFT"):
        if (self.menu_daf_x == 1):
          self.menu_daf_x = 0
          self.display.render_delete_all_files(True)
      
      if (button_pressed == "RIGHT"):
        if (self.menu_daf_x == 0):
          self.menu_daf_x = 1
          self.display.render_delete_all_files()

      if (button_pressed == "CENTER"):
        if (self.menu_daf_x == 0):
          self.main.utils.delete_all_files()
          # utils will control deleting files progress page

        if (self.menu_daf_x == 1):
          self.main.active_menu = "Settings"
      
    self.main.processing = False
    self.update_menu(button_pressed)

  def update_menu(self, button):
    if (self.main.active_menu == "Home"):
      if (self.menu_x == 0 and self.menu_y == 0):
        self.display.draw_active_icon("Files")

        if (button == "CENTER"):
          self.display.render_files()

      if (self.menu_x == -1 and self.menu_y == 0):
        self.display.draw_active_icon("Camera Settings")

      if (self.menu_y == -1 or self.menu_y == -2):
        self.display.draw_active_icon("Photo Video Toggle")

        if (button == "CENTER"):
          self.camera.change_mode("video")
          self.display.toggle_text("video") # what
          self.main.active_menu = "Video"
        
        if (button == "BACK"):
          self.camera.change_mode("small")
          self.display.toggle_text("photo")
          self.main.active_menu = "Home"

      if (self.menu_x == 1 and self.menu_y == 0):
        self.display.draw_active_icon("Settings")

        if (button == "CENTER"):
          self.display.render_settings()
          self.display.draw_active_telemetry()
          self.main.active_menu = "Settings"

    if (self.main.active_menu == "Settings"):
      if (self.menu_settings_y == 0):
        self.display.render_settings()
      
      if (self.menu_settings_y == 1):
        self.display.draw_active_telemetry()
        self.active_menu_item = "Telemetry"

      if (self.menu_settings_y == 2):
        self.display.render_settings()
        self.display.draw_active_battery_profiler()
        self.active_menu_item = "Battery Profiler"

      if (self.menu_settings_y == 3):
        self.display.render_settings()
        self.display.draw_active_reset_battery()
        self.active_menu_item = "Reset Battery"

      if (self.menu_settings_y == 4):
        self.display.render_settings()
        self.display.draw_active_timelapse()
        self.active_menu_item = "Timelapse"

      if (self.menu_settings_y == 5):
        self.display.render_settings()
        self.display.draw_active_transfer_to_usb()
        self.active_menu_item = "Transfer To USB"
      
      if (self.menu_settings_y == 6):
        self.display.render_settings()
        self.display.draw_active_delete_all_files()
        self.active_menu_item = "Delete All Files"

    if (self.main.active_menu == "Files"):
      if (button == "BACK"):
        self.main.active_menu = "Home"
        self.display.start_menu()

      if (self.files_y == 0): # footer
        print('navigate files')
        # future is view full size, delete
      else: # thumbnails
        print('navigate footer/pagination')

    if (self.main.active_menu == "Video"):
      if (button == "SHUTTER"):
        if (not self.recording_video):
          self.display.clear_screen()
          self.camera.start_video_recording()
          self.recording_video = True
        else:
          self.camera.stop_video_recording()
          self.recording_video = False
          self.display.draw_text("Recording saved")
          time.sleep(1)
          self.main.active_menu = "Home"
          self.display.start_menu()

    if (self.main.active_menu == "Battery Profiler"):
      if (button == "BACK"):
        self.main.battery.stop_profiler()
        self.main.active_menu = "Home"
        self.main.battery_profiler_active = False
        self.display.start_menu()
    
    if (self.main.active_menu == "Reset Battery"):
      if (button == "BACK"):
        self.main.active_menu = "Home"
        self.display.start_menu()

    if (self.main.active_menu == "Timelapse"):
      if (button == "BACK"):
        self.main.camera.stop_timelapse()
        self.main.active_menu = "Home"
        self.display.start_menu()

    if (self.main.active_menu == "Battery Charged"):
      if (button == "LEFT" and not self.battery_charged):
        self.battery_charged = True
        self.display.render_battery_charged(True)

      if (button == "CENTER"):
        if (self.battery_charged):
          self.main.battery.reset_uptime()

        self.main.active_menu = "Home"
        self.display.start_menu()

    self.main.processing = False
