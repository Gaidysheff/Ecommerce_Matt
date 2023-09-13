from django.contrib import admin
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund


def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


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
    list_display = ('id', 'user', 'ref_code', 'start_date', 'ordered_date', 'ordered',
                    'shipping_address', 'billing_address',
                    'payment', 'coupon', 'being_delivered', 'received',
                    'refund_requested', 'refund_granted')
    # 'display_orders',
    list_display_links = ('id', 'user', 'shipping_address',
                          'billing_address', 'payment', 'coupon', )
    search_fields = ('user__username', 'ref_code', )
    list_editable = ('ordered', 'being_delivered',
                     'received', 'refund_requested', 'refund_granted')
    list_filter = ('start_date', 'ordered_date', 'ordered',
                   'being_delivered', 'received', 'refund_requested', 'refund_granted')
    actions = [make_refund_accepted]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'street_address', 'apartment_address',
                    'country', 'zip', 'address_type', 'default')
    search_fields = ('user', )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'stripe_charge_id', 'user', 'amount', 'timestamp')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'amount', )


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'reason', 'accepted', 'email', )
