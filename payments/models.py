from django.conf import settings
from django.db import models


class Payment(models.Model):
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE)
    provider = models.CharField(max_length=50)  # e.g., razorpay, cod
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.order} ({self.provider})"
