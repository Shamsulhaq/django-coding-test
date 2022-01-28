from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from product.views.product import CreateProductView, ProductView, ProductViewSet
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

router = DefaultRouter()
router.register(r'create', ProductViewSet, basename='products')

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('api/', include(router.urls)),
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('list/', ProductView.as_view(), name='list.product'),
    # path('', ProductCreateView.as_view(), name='save.product'),
]