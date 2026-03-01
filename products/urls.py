from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('<slug:slug>/', views.product_detail, name='detail'),
]