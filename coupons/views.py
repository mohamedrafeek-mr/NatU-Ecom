from django.shortcuts import redirect
from .models import Coupon


def apply_coupon(request):
    code = request.POST.get('code', '').strip()
    try:
        coupon = Coupon.objects.get(code__iexact=code, active=True)
    except Coupon.DoesNotExist:
        request.session['coupon_error'] = 'Invalid coupon'
        return redirect('cart:detail')
    if not coupon.is_valid():
        request.session['coupon_error'] = 'Coupon expired'
        return redirect('cart:detail')
    request.session['coupon_id'] = coupon.id
    request.session['coupon_success'] = f"Coupon '{coupon.code}' applied."
    return redirect('cart:detail')
