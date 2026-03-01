from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ecompro.cart.models import Cart
from .models import Order, OrderItem


@login_required
def create_order(request):
    cart = Cart.objects.filter(user=request.user).first() or Cart.objects.filter(pk=request.session.get('cart_id')).first()
    if not cart or not cart.items.exists():
        return redirect('cart:detail')
    # for simplicity take first address
    address = request.user.addresses.first()

    # calculate any coupon discount stored in session
    coupon = None
    discount_amount = 0
    coupon_id = request.session.pop('coupon_id', None)
    if coupon_id:
        from ecompro.coupons.models import Coupon
        try:
            coupon = Coupon.objects.get(pk=coupon_id)
            if coupon.is_valid():
                if coupon.discount_percent:
                    discount_amount = cart.total() * (coupon.discount_percent / 100)
                elif coupon.discount_amount:
                    discount_amount = coupon.discount_amount
                discount_amount = min(discount_amount, cart.total())
            else:
                coupon = None
        except Coupon.DoesNotExist:
            coupon = None

    order = Order.objects.create(
        user=request.user,
        address=address,
        coupon=coupon,
        discount_amount=discount_amount,
    )
    for item in cart.items.all():
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.sale_price)
    cart.items.all().delete()
    return redirect('orders:history')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-placed_at')
    return render(request, 'orders/history.html', {'orders': orders})
