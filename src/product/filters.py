from django_filters import *
from .models import Product
from django.db.models import Q


class ProductFilters(FilterSet):
    price_from = NumberFilter(field_name='productvariantprice__price', lookup_expr='gte', label="Price From")
    price_to = NumberFilter(field_name='productvariantprice__price', lookup_expr='lte', label="Price To")
    title = CharFilter(field_name='title', lookup_expr='icontains')
    variant = CharFilter(field_name='productvariant__variant_title', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = {'id', 'title', 'created_at'}