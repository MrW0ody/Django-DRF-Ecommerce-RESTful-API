from django.contrib import admin
from product.models import Category, Product, Brand, ProductLine

"""
admin.site.register(Category)
admin.site.register(ProductLine)
admin.site.register(Brand)
"""


class ProductLineInline(admin.TabularInline):
    model = ProductLine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'is_digital', 'is_active']
    list_filter = ['is_digital', 'is_active']
    search_fields = ['name', 'slug', 'description']
    inlines = [ProductLineInline]


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    list_display = ['price', 'sku', 'stock_qty', 'is_active']
    list_filter = ['price', 'is_active']
