import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Message


class ChatConsumer(WebsocketConsumer):

	def connect(self):
		self.chan_id = self.scope['url_route']['kwargs']['slug']
		async_to_sync(self.channel_layer.group_add)(
			self.chan_id,
			self.channel_name
		)
		self.accept()


	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.chan_id,
			self.channel_name
		)
		

	def receive(self, text_data):
		json_text_data = json.loads(text_data)
		message = json_text_data['message']

		Message.objects.create(
			chat_id=json_text_data['chat_id'], creator_id=json_text_data['user_id'], message=message
			)

		async_to_sync(self.channel_layer.group_send)(
			self.chan_id,
			{		
				'message': message,
				'user_id': json_text_data['user_id'],
				'type': 'chat_message'
			}
		)

	def chat_message(self, event):
		self.send(text_data=json.dumps(event))
		
