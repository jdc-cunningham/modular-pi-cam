import asyncio
import websockets

class WebSocket():
  def __init__(self, update_value):
    self.socket = None
    self.update_value = update_value

  async def recvd_msg(self, msg) -> bool:
    if ('iso' in msg):
      val = msg.split(',')[1]
      self.update_value('iso', val)

    if ('shutter' in msg):
      val = msg.split(',')[1]
      self.update_value('shutter', val)

  async def socket_listener(self, socket):
    while True:
      msg = await socket.recv()
      await self.recvd_msg(msg)
      await asyncio.sleep(0.1)

  async def socket_main(self):
    async with websockets.serve(self.socket_listener, "192.168.1.104", 5678):
      await asyncio.Future()

  def start(self):
     asyncio.run(self.socket_main())
