from django.shortcuts import render

from django.shortcuts import render

from ecompro.products.models import Product, Category


def home(request):
    # only show active featured products
    featured = Product.objects.filter(featured=True, status='active')[:5]
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'core/home.html', {'featured': featured, 'categories': categories})


def contact(request):
    return render(request, 'core/contact.html')


def about(request):
    return render(request, 'core/about.html')

