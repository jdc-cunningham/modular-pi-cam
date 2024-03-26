from picamera2 import Picamera2
from PIL import Image

picam2 = Picamera2()
full_config = picam2.create_still_configuration()
small_config = picam2.create_still_configuration(raw={"size": (4056, 2592)}, main={"size": (320, 320)})
picam2.configure(small_config)

picam2.start()

# picam2.set_controls({"ScalerCrop": (0, 0, 320, 320)})

# pil_img = picam2.capture_image()

# # https://stackoverflow.com/a/451580/2710227
# def scale_image(img, new_width):
#   base_width= new_width
#   wpercent = (base_width / float(img.size[0]))
#   hsize = int((float(img.size[1]) * float(wpercent)))
#   img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
#   img.save('resized.jpg')

# scale_image(pil_img, 320)

# picam2.switch_mode(big_config)

picam2.capture_file('scaled.jpg')