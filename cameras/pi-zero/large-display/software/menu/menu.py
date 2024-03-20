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
    self.active_menu_item = None
    self.files_page = 1 # this shouldn't be here
    self.files_pages = 1
    self.files_y = 0 # footer or files
    self.recording_video = False
    self.battery_charged = False # yes, no question

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

    if (self.main.active_menu == "Settings"):
      if (button_pressed == "DOWN" and self.menu_settings_y < 3):
        self.menu_settings_y += 1
      
      if (button_pressed == "UP" and self.menu_settings_y > 1):
        self.menu_settings_y -= 1

      if (button_pressed == "BACK"):
        if (self.active_menu_item == "Battery Profiler"):
          self.main.battery.stop_profiler()

        self.active_menu_item = None
        self.menu_settings_y = 0
        self.display.start_menu()
        self.main.active_menu = "Home"

      if (button_pressed == "CENTER"):
        if (self.active_menu_item == "Telemetry"):
          self.display.render_telemetry_page()
          self.main.processing = False
          return
    
        if (self.active_menu_item == "Battery Profiler"):
          self.display.render_battery_profiler()
          self.main.battery.start_profiler()
          self.main.battery_profiler_active = True
          self.main.processing = False
          return
      
        if (self.active_menu_item == "Timelapse"):
          self.main.active_menu = "Timelapse"
          self.display.render_timelapse()
          self.main.camera.start_timelapse()
          self.main.processing = False
          return

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
        self.display.draw_active_timelapse()
        self.active_menu_item = "Timelapse"

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
          self.display.draw_text("Recording video...")
          self.camera.start_video_recording()
          self.recording_video = True
        else:
          self.camera.stop_video_recording()
          self.recording_video = False
          self.display.draw_text("Recording saved")
          time.sleep(0.3)
          self.main.active_menu = "Home"
          self.display.start_menu()

    if (self.main.active_menu == "Battery Profiler"):
      if (button == "BACK"):
        self.main.battery.stop_profiler()
        self.main.active_menu = "Home"
        self.main.battery_profiler_active = False
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
