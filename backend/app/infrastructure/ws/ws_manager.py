import asyncio

class WebSocketManager:
    def __init__(self):
        self.connections = []
        self.loop = None

    def set_loop(self, loop):
        self.loop = loop

    async def connect(self, websocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message):
        for conn in self.connections:
            try:
                await conn.send_json(message)
            except:
                pass

    def send(self, message):
        if self.loop:
            asyncio.run_coroutine_threadsafe(
                self.broadcast(message),
                self.loop
            )

ws_manager = WebSocketManager()
