from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products',views.ProductViewSet)
router.register('meals',views.MealViewSet)
router.register('supervisionoffices',views.SupervisionOfficeViewSet)
router.register('orders',views.OrderViewSet)
router.register('search', views.SearchViewSet)
router.register('order_products', views.OrderProductShipViewSet)
router.register('order_meals', views.OrderMealShipViewSet)
# router.register('shoppingcarts',views.ShoppingCartViewSet)
# router.register('product_images',views.ProductImageViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('get_current_version', views.AppVersionView.as_view()),
]