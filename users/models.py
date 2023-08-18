from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse
from django.utils.text import slugify
from django.db import models
from django.conf import settings

from datetime import datetime


# Create your models here.
class Profile(models.Model):
	# base
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
	# picture
	picture = models.ImageField(null=True, blank=True, upload_to='imgs/profile_pics/')

	# additional
	description = models.TextField(blank=True, null=True)
	imlookingfor = models.TextField(blank=True, null=True)

	birth_date = models.DateTimeField(blank=True, null=True)
	education = models.CharField(max_length=200, blank=True, null=True)

	age = models.IntegerField(blank=True, null=True)

	# answers_limit = models.IntegerField(blank=True, null=True, default=30)

	# my portfolio links (links)
	


	def __str__(self):
		return self.user.username
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user)

		if self.birth_date != None:
			self.age = int(int(datetime.now().timestamp() - self.birth_date.timestamp())/60/60/24/365)

		super().save(*args, **kwargs)		

	def get_absolute_url(self):
		return reverse('users:profile_other', args=[self.slug])
	
	def get_my_chats(self):
		chats1 = self.chats1.all()
		chats2 = self.chats2.all()
		return chats1.union(chats2)


class Chat(models.Model):
	usr1 = models.ForeignKey(Profile, related_name='chats1', on_delete=models.DO_NOTHING)
	usr2 = models.ForeignKey(Profile, related_name='chats2', on_delete=models.DO_NOTHING)

	created = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=100)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(f'{self.usr1}&{self.usr2}')
		super().save(*args, **kwargs)

	def get_chat(user_one, user_two):
		try:
			chat = Chat.objects.get(usr1=user_one, usr2=user_two)
		except ObjectDoesNotExist:
			try:
				chat = Chat.objects.get(usr1=user_two, usr2=user_one)
			except:
				chat = Chat.objects.create(usr1=user_one, usr2=user_two)
			
		return chat

	def get_oposite_user(self, request):
		if self.usr1 != request.user.profile:
			return self.usr1
		return self.usr2


class Message(models.Model):
	chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.DO_NOTHING)
	creator = models.ForeignKey(Profile, related_name='messages', on_delete=models.DO_NOTHING)
	message = models.TextField()
	is_read = models.BooleanField(default=False)

	created = models.DateTimeField(auto_now_add=True)
