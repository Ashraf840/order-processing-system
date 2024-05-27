from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock']
    list_display_links = ['name']
    search_fields = ['id', 'name']
    # readonly_fields = ['created_at', 'last_updated_at']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    list_filter = ['price', 'stock']
    list_per_page = 15
    ordering = ['name']

admin.site.register(Product, ProductAdmin)