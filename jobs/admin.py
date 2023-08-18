from django.contrib import admin
from .models import Job, Requirements, TimeType, Location, Comment, JobAnswer


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
	list_display = ('job_title','salary' ,'location', 'salary', 'created', 'owner', 'updated', 'type')


@admin.register(Requirements)
class RequirementsAdmin(admin.ModelAdmin):
	list_display = ('name', )


@admin.register(TimeType)
class TimeTypeAdmin(admin.ModelAdmin):
	pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('comment', 'creator', 'created')


@admin.register(JobAnswer)
class JobAnswerAdmin(admin.ModelAdmin):
	list_display = ('created', 'job', 'creator')
