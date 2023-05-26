from django.contrib import admin
from orders.models import Payment, Order, OrderedItem

class OrderedItemInline(admin.TabularInline):
    model = OrderedItem
    readonly_fields = ('order', 'payment', 'user', 'item', 'session', 'fee', 'amount')
    extra = 0

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_id', 'payment_method', 'amount', 'status', 'receiver', 'created_at']
    # readonly_fields = ('transaction_id', 'payment_method', 'amount', 'status', 'created_at')
    # list_filter = ['status', 'payment_method']
    # search_fields = ['user', 'payment_id']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'order_placed_to', 'is_ordered']
    inlines = [OrderedItemInline]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem)


    