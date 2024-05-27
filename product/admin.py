from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'stock']
    list_display_links = ['name']
    search_fields = ['id', 'name']
    # readonly_fields = ['created_at', 'last_updated_at']
    filter_horizontal = []
    fieldsets = []
    list_filter = ['price', 'stock']
    list_per_page = 15
    ordering = ['name']

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductAttribute)
admin.site.register(AttributeValue)
admin.site.register(Product)
admin.site.register(ProductLine)