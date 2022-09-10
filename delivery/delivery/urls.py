from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
	path('organizations/', include('places.urls', namespace='places')),


	path('', include('catalog.urls', namespace='catalog')),

]
