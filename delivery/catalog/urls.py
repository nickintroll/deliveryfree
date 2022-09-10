from django.urls import path
from .views import catalog_view, product_detail


app_name='catalog'
urlpatterns = [
    path('', catalog_view, name='catalog'),
	path('prod/<slug:slug>/', product_detail, name='product_detail'),
]
