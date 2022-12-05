"""
All the connections of the apps are listed here.
"""
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, Thread, Message
from channels.db import database_sync_to_async
from datetime import datetime
from channels.exceptions import DenyConnection



class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_thread(self):
        return Thread.objects.get(pk=self.pk)

    @database_sync_to_async
    def get_user(self, pk=None):
        if pk:
            user = User.objects.get(pk=pk)
            user.is_deleted = True
            user.save()
        return User.objects.get(pk=self.user_id)

    @database_sync_to_async
    def store_agent_in_thread(self):
        return self.thread.save()

    @database_sync_to_async
    def save_message(self):
        message = Message(message_body=self.message, sender_id=self.thread.client_id, thread_id=self.thread.id, is_read=True)
        return message.save()

    @database_sync_to_async
    def save_end_time(self):
        return self.thread.save()

    @database_sync_to_async
    def get_message(self):
        messages = Message.objects.filter(thread_id=self.thread.id, sender_id=self.thread.client_id)
        mes_list = []
        for message in messages:
            dicts ={}
            dicts["message"] = message.message_body
            dicts["date"] = str(message.timestamp)
            mes_list.append(dicts)
        return mes_list    

    async def connect(self):
        self.pk = self.scope["url_route"]["kwargs"]["pk"]
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.user = await self.get_user()
        self.thread = await self.get_thread()
        count = self.thread.count
        count +=1
        if count >=2:
            self.room_group_name = str(self.thread.agent_id)+"and"+str(self.thread.client_id)
            raise DenyConnection("This conversation thread is already close.")
        self.thread.count = count
        self.thread.agent_id = self.user_id
        await self.store_agent_in_thread()
        self.room_group_name = str(self.thread.agent_id)+"and"+str(self.thread.client_id)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        messages = await self.get_message()
        for mes in messages:
            await self.send(text_data=json.dumps({"message": mes["message"], "date": mes["date"]}))

    async def disconnect(self, close_code):
        # Leave room group
        self.thread.end_time = datetime.now()
        client_id = self.thread.client_id
        await self.get_user(pk=client_id)
        await self.save_end_time()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json["message"]
        self.date = text_data_json["date"]
        await self.save_message()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": self.message, "date": self.date}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        date = event["date"]
        await self.send(text_data=json.dumps({"message": message, "date": date}))


