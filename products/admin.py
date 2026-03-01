from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'featured', 'status', 'view_on_site_link')
    list_filter = ('status', 'category', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    def view_on_site_link(self, obj):
        return format_html('<a href="{}" target="_blank">View</a>', obj.get_absolute_url())
    view_on_site_link.short_description = 'Website'
