
from threading import Thread
from websocket.websocket import WebSocket
from videostream.videostream import *

socket = WebSocket()

Thread(target=socket.start).start()

start_video_stream()