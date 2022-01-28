from django.contrib import admin

# Register your models here.
from .models import Product, ProductVariant, Variant, ProductVariantPrice, ProductImage

admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(ProductVariantPrice)
admin.site.register(Variant)
admin.site.register(ProductImage)