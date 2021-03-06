from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products',views.ProductViewSet)
router.register('product_images',views.ProductImageViewSet)
router.register('supervisionoffices',views.SupervisionOfficeViewSet)
router.register('orders',views.OrderViewSet)
router.register('shoppingcarts',views.ShoppingCartViewSet)
router.register('search', views.SearchViewSet)
router.register('order_products', views.OrderProductShipViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]