from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
	path('', views.jobs_search_main_page, name='main'), 
	path('new/', views.creating_job, name='creation'), 

	path('edit/<slug:slug>/', views.edit, name='edit'), 
	# path('answer/<slug:slug>/<int:answer_comment_id>/', views.detail, name='answer_comment'),

	path('<slug:slug>/', views.detail, name='detail'), 
	
]