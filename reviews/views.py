from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Review
from ecompro.products.models import Product


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
    return redirect(product.get_absolute_url())
