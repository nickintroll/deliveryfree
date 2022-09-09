from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display=['title', 'slug', 'price',]
	prepopulated_fields = {'slug': ('title', 'price')}

