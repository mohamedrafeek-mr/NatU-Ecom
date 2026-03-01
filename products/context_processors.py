from .models import Category


def all_categories(request):
    """Make the full category hierarchy available to all templates.

    We return a queryset of top-level categories; templates can traverse
    `children` for sub‑categories if desired.
    """
    cats = Category.objects.filter(parent__isnull=True).order_by('name')
    current = request.path
    # mark selected categories based on the current path
    for cat in cats:
        cat.selected = current.startswith(cat.get_absolute_url())
        for child in cat.children.all():
            child.selected = current.startswith(child.get_absolute_url())
    return {'all_categories': cats}
