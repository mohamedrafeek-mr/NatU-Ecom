from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey('accounts.Address', on_delete=models.SET_NULL, null=True)
    # optional coupon applied to order
    coupon = models.ForeignKey('coupons.Coupon', null=True, blank=True, on_delete=models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.pk} ({self.user})"

    def total(self):
        total = sum(item.subtotal() for item in self.items.all())
        return total - self.discount_amount


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    SHIPPING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    shipping_status = models.CharField(max_length=20, choices=SHIPPING_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    def subtotal(self):
        return self.quantity * self.price


def _recalculate_order_status(order):
    items = order.items.all()
    if not items.exists():
        return
    statuses = [it.shipping_status for it in items]
    # If all items are cancelled => order cancelled
    if all(s == 'cancelled' for s in statuses):
        new_status = 'cancelled'
    else:
        # ignore cancelled items when determining overall progress
        non_cancelled = [s for s in statuses if s != 'cancelled']
        priority = {'pending': 1, 'processing': 2, 'shipped': 3, 'delivered': 4}
        # pick the least-advanced status (min priority) so outstanding items keep order in earlier state
        min_status = min(non_cancelled, key=lambda s: priority.get(s, 1))
        new_status = min_status
    if order.status != new_status:
        order.status = new_status
        order.save(update_fields=['status'])


@receiver(post_save, sender=globals().get('OrderItem'))
def _orderitem_saved(sender, instance, **kwargs):
    try:
        _recalculate_order_status(instance.order)
    except Exception:
        pass


@receiver(post_delete, sender=globals().get('OrderItem'))
def _orderitem_deleted(sender, instance, **kwargs):
    try:
        _recalculate_order_status(instance.order)
    except Exception:
        pass
