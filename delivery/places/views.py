from django.shortcuts import render
from .models import Organization


def places_list(request):
	places = Organization.objects.all()
	return render(request, 'places/places_list.html', {'places': places})


def place_detail(request, slug):
	place = Organization.objects.get(slug=slug)
	return render(request, 'places/place_detail.html', {'place': place})
