from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'shipping_status')
    readonly_fields = ()


# `Order` is intentionally not registered in the admin per request.
# If another module registered it, ensure it's unregistered to hide it from admin.
from django.contrib.admin.sites import NotRegistered

try:
    admin.site.unregister(Order)
except Exception:
    # If it's not registered, ignore the error.
    pass


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'shipping_status')
    list_filter = ('shipping_status',)
    actions = ['mark_shipped', 'mark_delivered']

    def mark_shipped(self, request, queryset):
        # Use per-instance save() so post_save signal runs and order status recalculates
        count = 0
        for item in queryset.select_related('order'):
            item.shipping_status = 'shipped'
            item.save()
            count += 1
        self.message_user(request, f"Marked {count} item(s) as shipped.")

    def mark_delivered(self, request, queryset):
        # Use per-instance save() so post_save signal runs and order status recalculates
        count = 0
        for item in queryset.select_related('order'):
            item.shipping_status = 'delivered'
            item.save()
            count += 1
        self.message_user(request, f"Marked {count} item(s) as delivered.")

    mark_shipped.short_description = 'Mark selected items as shipped'
    mark_delivered.short_description = 'Mark selected items as delivered'


admin.site.register(OrderItem, OrderItemAdmin)
