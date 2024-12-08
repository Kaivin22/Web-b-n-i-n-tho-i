# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class InvoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Kết nối với WebSocket
        self.room_name = "invoice"
        self.room_group_name = f"invoice_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Rời khỏi group khi ngắt kết nối
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Nhận message từ WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        invoice_data = text_data_json['invoice_data']

        # Gửi message tới group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_invoice',
                'invoice_data': invoice_data
            }
        )

    # Nhận message từ group và gửi lại cho WebSocket
    async def send_invoice(self, event):
        invoice_data = event['invoice_data']

        # Gửi message đến WebSocket
        await self.send(text_data=json.dumps({
            'invoice_data': invoice_data
        }))