from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create'),
    path('history/', views.order_history, name='history'),
]