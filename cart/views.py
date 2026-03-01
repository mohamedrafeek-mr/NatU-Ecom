from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem
from ecompro.products.models import Product


def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(pk=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.pk
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.pk
    return cart


def cart_detail(request):
    cart = _get_cart(request)

    # coupon handling
    coupon = None
    discount = 0
    coupon_error = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        from ecompro.coupons.models import Coupon
        try:
            coupon = Coupon.objects.get(pk=coupon_id)
            if coupon.is_valid():
                if coupon.discount_percent:
                    discount = cart.total() * (coupon.discount_percent / 100)
                elif coupon.discount_amount:
                    discount = coupon.discount_amount
                # don't let discount exceed cart total
                discount = min(discount, cart.total())
            else:
                coupon_error = 'Coupon expired'
                # invalid coupon, clear it
                del request.session['coupon_id']
                coupon = None
                discount = 0
        except Coupon.DoesNotExist:
            coupon_error = 'Invalid coupon'
            del request.session['coupon_id']

    # pop any coupon error/success messages set by apply_coupon view
    coupon_error = coupon_error or request.session.pop('coupon_error', None)
    coupon_success = request.session.pop('coupon_success', None)

    total = cart.total()
    total_after_discount = total - discount

    context = {
        'cart': cart,
        'coupon': coupon,
        'discount': discount,
        'total_after_discount': total_after_discount,
        'coupon_error': coupon_error,
        'coupon_success': coupon_success,
    }
    return render(request, 'cart/detail.html', context)



def add_to_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart:detail')


def buy_now(request, product_id):
    """Add the product and redirect straight to checkout/create order."""
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_id)
    # override quantity to 1 so buy now always purchases a single item
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity = 1
    item.save()
    # redirect to order creation (will require login)
    from django.urls import reverse
    return redirect(reverse('orders:create'))



def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect('cart:detail')


def update_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart:detail')
