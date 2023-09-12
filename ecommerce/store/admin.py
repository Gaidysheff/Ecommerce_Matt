from django.contrib import admin
from .models import Item, OrderItem, Order, Address, Payment


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'discount_price',
                    'category', 'label', 'slug', 'description', 'image')
    list_display_links = ('id', 'title', 'category', 'label', 'description')
    search_fields = ('title', 'category', 'label', 'description')
    list_filter = ('title', 'price', 'category', 'label')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered', 'item', 'quantity')
    list_display_links = ('id', 'item')
    search_fields = ('user', 'item')
    list_editable = ('ordered',)
    list_filter = ('ordered',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_orders',
                    'start_date', 'ordered_date', 'ordered', 'shipping_address', 'billing_address', 'payment',)
    list_display_links = ('id', 'display_orders')
    search_fields = ('user', )
    list_editable = ('ordered',)
    list_filter = ('start_date', 'ordered_date', 'ordered')


@admin.register(Address)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'street_address', 'apartment_address',
                    'country', 'zip', 'address_type', 'default')
    search_fields = ('user', )


@admin.register(Payment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_charge_id', 'user', 'amount', 'timestamp')
