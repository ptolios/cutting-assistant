from django.contrib import admin
from .models import Order, OrderItem


class OrderItemTabularInline(admin.TabularInline):
   model = OrderItem
   extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemTabularInline]

    list_display = (
        'customer',
        'placement_datetime',
        'delivery_date',
        'status'
    )


admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem)
