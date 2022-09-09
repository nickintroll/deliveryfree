from django.shortcuts import render
from .models import Product

def catalog_view(request):

	prods = Product.objects.all()

	return render(request, 'catalog/catalog.html', {'prods':prods})

def product_detail(request, slug):

	product = Product.objects.get(slug=slug)

	return render(request, 'catalog/catalog_prod.html', {'prod': product})
