from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name='users'
urlpatterns = [
	path('login/', views.login_page, name='login'),
	path('register/', views.register_page, name='register'),
	path('profile/', views.profile_page, name='profile'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('oth/<slug:slug>', views.profile_page, name='profile_other'),
	path('list/', views.users_list, name='list'),
	path('update/', views.update_profile, name='update_profile'),
	path('chat/<slug:chat>', views.chat_room, name='chat_room'),

	path('chat_in/<slug:usr1>', views.chat_room_enter ,name='chat_room_enter'),
]
