import asyncio
import websockets

class WebSocket():
  def __init__(self):
     self.socket = None

  async def recvd_msg(msg, socket):
      print(msg)

  async def socket_listener(self, socket):
    while True:
      msg = await socket.recv()
      print('recvd msg' + msg)
      self.recvd_msg(msg)
      await asyncio.sleep(0.1)

  async def socket_main(self):
    print('run socket')
    async with websockets.serve(self.socket_listener, "192.168.1.104", 5678):
      await asyncio.Future()

  def start(self):
     asyncio.run(self.socket_main())
