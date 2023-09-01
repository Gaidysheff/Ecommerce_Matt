from django.contrib import admin
from .models import Item, OrderItem, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount_price',
                    'category', 'label', 'slug')
    list_display_links = ('id', 'title', 'category', 'label')
    search_fields = ('title', 'category', 'label')
    list_filter = ('title', 'price', 'category', 'label')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered', 'item')
    list_display_links = ('id', 'item')
    search_fields = ('user', 'item')
    list_editable = ('ordered',)
    list_filter = ('ordered',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_orders',
                    'start_date', 'ordered_date', 'ordered',)
    list_display_links = ('id', 'display_orders')
    search_fields = ('user', )
    list_editable = ('ordered',)
    list_filter = ('start_date', 'ordered_date', 'ordered')
