
from threading import Thread
from websocket.websocket import WebSocket
from videostream.videostream import *

# update_camera_values from videostream
socket = WebSocket(update_camera_values)

Thread(target=socket.start).start()

start_video_stream()