from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'line1', 'city', 'postal_code')
