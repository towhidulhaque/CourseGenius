from channels.generic.websocket import AsyncWebsocketConsumer


class CoreConsumer(AsyncWebsocketConsumer):
    """Basic consumer class."""

    async def connect(self):
        """Connect into group."""
        self.ping_pong_group = 'ping_pong_group'
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.ping_pong_group, self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Leave group."""
        await self.channel_layer.group_discard(
            self.ping_pong_group, self.channel_name,
        )
