from django.shortcuts import get_object_or_404, render

from .models import Product, Category
from django.http import JsonResponse


# new autocomplete endpoint used by the search input

def autocomplete(request):
    """Return a small JSON list of product names matching the query.

    The frontend uses the names to populate a <datalist> while the user types.
    """
    q = request.GET.get('q', '').strip()
    suggestions = []
    if q:
        matches = (
            Product.objects
            .filter(name__icontains=q, stock__gt=0, status='active')
            .values_list('name', flat=True)[:10]
        )
        suggestions = list(matches)
    return JsonResponse({'suggestions': suggestions})


def product_list(request):
    # basic list with optional search query
    q = request.GET.get('q', '').strip()
    products = Product.objects.filter(stock__gt=0, status='active')
    if q:
        # filter by name containing the query (case‑insensitive)
        products = products.filter(name__icontains=q)
    context = {'products': products, 'q': q}
    return render(request, 'products/list.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(stock__gt=0, status='active')
    return render(request, 'products/category.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, status='active')
    # coupon messages
    coupon_error = request.session.pop('coupon_error', None)
    coupon_success = request.session.pop('coupon_success', None)
    # related products: other active products in same category, exclude current
    related = Product.objects.filter(category=product.category, status='active').exclude(pk=product.pk)[:8]
    context = {
        'product': product,
        'coupon_error': coupon_error,
        'coupon_success': coupon_success,
        'related_products': related,
    }
    return render(request, 'products/detail.html', context)
