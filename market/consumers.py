import json, asyncio, random
from channels.generic.websocket import AsyncWebsocketConsumer

class MarketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "market_updates"

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        print(f"✅ WebSocket connected: {self.channel_name}")

        await self.send(text_data=json.dumps({
            "message": "📊 Connected to live Nifty 50 updates!"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"❌ WebSocket disconnected: {self.channel_name}")

    async def market_update(self, event):
        """Receive broadcast from background task."""
        print("📡 Received event in consumer:", event["data"])
        await self.send(text_data=json.dumps(event["data"]))