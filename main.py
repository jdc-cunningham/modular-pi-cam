
from threading import Thread
from websocket.websocket import WebSocket
from videostream.videostream import VideoStream

socket = WebSocket()
video = VideoStream()

Thread(target=socket.start).start()
Thread(target=video.start).start()