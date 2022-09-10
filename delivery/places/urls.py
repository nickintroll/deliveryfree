from django.urls import path
from .views import places_list, place_detail 


app_name = 'places'
urlpatterns = [
	path('', places_list, name='catalog'),
	path('<slug:slug>/', place_detail, name='place_detail')
]