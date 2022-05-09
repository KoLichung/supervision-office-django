from unicodedata import category
from httplib2 import Authentication
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

from modelCore.models import Category , Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip , Order , ShoppingCart
from api import serializers

class CategoryViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

#http://localhost:8000/api/products/?suppervision_office_id=1&category_id=2
class ProductViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    #query by suppervision office and category
    def get_queryset(self):
        queryset = self.queryset
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')
        category_id = self.request.query_params.get('category_id')
        #get suppervion offices all products
        theSuppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
        productsIds = ProductSupervisionOfficeShip.objects.filter(supervisionOffice=theSuppervisionOffice).values_list('product',flat=True)
        queryset = queryset.filter(pk__in=productsIds)
        #filter by category
        queryset = queryset.filter(category=Category.objects.get(id=category_id))
        
        for i in range(len(queryset)):
            if ProductImage.objects.filter(product=queryset[i]).count()!=0:
                queryset[i].coverImage = ProductImage.objects.filter(product=queryset[i]).first().image

        return queryset


class ProductImageViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = serializers.ProductImageSerializer

    def get_queryset(self):
        queryset = self.queryset
        product_id = self.request.query_params.get('product_id')
        theProduct = Product.objects.get(id=product_id)
        queryset = queryset.filter(product=theProduct)
        return queryset

    #query by product

class SupervisionOfficeViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,):

    queryset = SupervisionOffice.objects.all()
    serializer_class = (serializers.SupervisionOfficeSerializer)


# class ProductSupervisionOfficeShipViewSet(viewsets.GenericViewSet,
#                                             mixins.ListModelMixin,
#                                             mixins.RetrieveModelMixin,
#                                             mixins.CreateModelMixin,
#                                             mixins.UpdateModelMixin):
#     queryset = ProductSupervisionOfficeShip.objects.all()
#     serializer_class = serializers.ProductSuperofficeShipSerializer


class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    autheneication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

class ShoppingCartViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin):
    autheneication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = ShoppingCart.objects.all()
    serializer_class = serializers.ShoppingCartSerializer

