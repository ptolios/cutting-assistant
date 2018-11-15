from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer',
        'placement_datetime',
        'delivery_date',
        'status'
    )


admin.site.register(Order, OrderAdmin)
