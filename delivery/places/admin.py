from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', 'location')}
	list_display = ('name', 'location')
