from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ecompro.core.urls')),
    path('accounts/', include('ecompro.accounts.urls')),
    path('accounts/', include('allauth.urls')),

    path('products/', include('ecompro.products.urls')),
    path('cart/', include('ecompro.cart.urls')),
    path('orders/', include('ecompro.orders.urls')),
    path('payments/', include('ecompro.payments.urls')),
    path('reviews/', include('ecompro.reviews.urls')),
    path('coupons/', include('ecompro.coupons.urls')),
    path('dashboard/', include('ecompro.dashboard.urls')),
]

# serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
