from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['user']
    search_fields = ['id']
    # readonly_fields = ['created_at', 'last_updated_at']  # to view these fields in the "(Food) Category" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields.
    filter_horizontal = []
    fieldsets = []
    # list_filter = ['is_ordered', 'created_at', 'last_updated_at']
    list_per_page = 15
    ordering = ['user']

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentInformation)
