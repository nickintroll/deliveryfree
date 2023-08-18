from django.contrib import admin
from .models import Profile, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('chat_id', 'creator', 'message')

