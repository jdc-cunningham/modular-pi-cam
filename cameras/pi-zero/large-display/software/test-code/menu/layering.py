from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont

font_path = "../../display/"

battery_sprite_path = "../../menu/menu-sprites/battery_25_15.jpg"
folder_sprite_path = "../../menu/menu-sprites/folder_21_18.jpg"
gear_sprite_path = "../../menu/menu-sprites/gear_23_20.jpg"

small_font = ImageFont.truetype(font_path + "alt-font.ttc", 13)
large_font = ImageFont.truetype(font_path + "alt-font.ttc", 16)

# this code can be ran on windows/host computer side
# easier than trying to run on pi (starting/stopping physical OLED)

def render_menu():
  image = Image.new("RGB", (128, 128), "BLACK")
  draw = ImageDraw.Draw(image)

  draw.text((7, 3), "video", fill = "WHITE", font = small_font)
  draw.text((7, 90), "S: 1/60", fill = "WHITE", font = small_font)
  draw.text((7, 105), "E: 100", fill = "WHITE", font = small_font)
  draw.text((22, 48), "Camera on", fill = "WHITE", font = large_font)
  draw.text((66, 3), "3 hrs", fill = "WHITE", font = small_font)
  draw.text((60, 103), "24", fill = "WHITE", font = small_font)

  battery_icon = Image.open(battery_sprite_path)
  folder_icon = Image.open(folder_sprite_path)
  gear_icon = Image.open(gear_sprite_path)

  image.paste(battery_icon, (98, 5))
  image.paste(folder_icon, (77, 103))
  image.paste(gear_icon, (101, 103))

  image.save("menu.jpg")

def render_settings():
  image = Image.new("RGB", (128, 128), "BLACK")
  draw = ImageDraw.Draw(image)

  draw.line([(0, 0), (128, 0)], fill = "WHITE", width = 40)
  draw.text((5, 0), "Settings", fill = "BLACK", font = large_font)
  draw.text((5, 26), "Telemetry", fill = "WHITE", font = large_font)

  image.save("settings.png")

render_settings()