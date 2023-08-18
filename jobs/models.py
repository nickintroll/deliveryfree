from django.urls import reverse
from django.utils.text import slugify
from django.db import models

from users.models import Profile

job__status_choices = (
	('Publish', 'Publish'), 
	('Not publish', 'Not publish' )
)


class TimeType(models.Model):
	type = models.CharField(max_length=120, default='-')
	def __str__(self):
		return self.type


class Requirements(models.Model):
	name = models.CharField(max_length=120, default='-')
	def __str__(self):
		return self.name


class Location(models.Model):
	name = models.CharField(max_length=120, default='-')
	def __str__(self):
		return self.name


class Job(models.Model):
	# title = models.CharField(max_length=120)
	job_title = models.CharField(max_length=120)
	slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

	owner = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='jobs')
	location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
	
	description = models.TextField()
	salary = models.FloatField()
	requirements = models.ManyToManyField(Requirements, blank=True)

	type = models.ForeignKey(TimeType, on_delete=models.DO_NOTHING)	
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	status = models.CharField(max_length=50, choices=job__status_choices, default='Publish')

	class Meta:
		ordering = ('-created', )

	def __str__(self):
		return self.job_title

	def save(self, *args, **kwargs):
		if self.slug == None:
			self.slug = slugify(f'{self.job_title}_{self.location}_{self.salary}')
		return super().save(*args, **kwargs)
	
	def get_absolute_url(self):
		return reverse('jobs:detail', args=[self.slug])


class Comment(models.Model):
	job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, related_name='comments')
	creator = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='comments')
	created = models.DateTimeField(auto_now_add=True)

	is_answer = models.BooleanField(default=False)
	answer_to = models.ForeignKey('Comment', on_delete=models.DO_NOTHING, related_name='answers', blank=True, null=True)

	comment = models.TextField()

	def get_comment_level(self):
		if not self.is_answer:
			return 0
		else:
			return 1 + self.answer_to.get_comment_level()


class JobAnswer(models.Model):
	job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, related_name='answers')
	creator = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='answers')
	created = models.DateTimeField(auto_now_add=True)

	is_viewed = models.BooleanField(default=False)
	description = models.TextField()

