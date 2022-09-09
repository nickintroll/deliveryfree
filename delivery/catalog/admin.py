from django.contrib import admin
from .models import Product, Image


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display=['title', 'slug', 'price',]
	prepopulated_fields = {'slug': ('title', 'price')}


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
	list_display=['product', 'image']



