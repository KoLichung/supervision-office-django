from unicodedata import category
from httplib2 import Authentication
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
# Create your views here.

from modelCore.models import Category, Product, SupervisionOffice, Order, User, ProductOrderShip, Meal, MealOrderShip
from modelCore.models import AppVersion, OutsideProduct, OutsideProductOrderShip, OutsideCategory, ConfigData, Announcement
from api import serializers

class CategoryViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        queryset = self.queryset
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')

        if suppervision_office_id!=None:
            suppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
            queryset = queryset.filter(suppervisionOffice=suppervisionOffice)

        return queryset

class OutsideCategoryViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = OutsideCategory.objects.all()
    serializer_class = serializers.OutsideCategorySerializer

    def get_queryset(self):
        queryset = self.queryset
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')

        if suppervision_office_id!=None:
            suppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
            queryset = queryset.filter(suppervisionOffice=suppervisionOffice)

        return queryset

#http://localhost:8000/api/products/?suppervision_office_id=1&category_id=1
class ProductViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    #query by suppervision office and category
    def get_queryset(self):
        queryset = self.queryset.filter(isPublish=True)
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')
        category_id = self.request.query_params.get('category_id')

        if suppervision_office_id!=None:
            suppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
            queryset = queryset.filter(suppervisionOffice=suppervisionOffice)

        if category_id!=None:
            category = Category.objects.get(id=category_id)
            queryset = queryset.filter(category=category)

        return queryset

class OutsideProductViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    queryset = OutsideProduct.objects.all()
    serializer_class = serializers.OutsideProductSerializer

    #query by suppervision office and category
    def get_queryset(self):
        queryset = self.queryset.filter(isPublish=True)
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')
        outside_category_id = self.request.query_params.get('outside_category_id')

        if suppervision_office_id!=None:
            suppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
            queryset = queryset.filter(suppervisionOffice=suppervisionOffice)

        if outside_category_id!=None:
            category = OutsideCategory.objects.get(id=outside_category_id)
            queryset = queryset.filter(outside_category=category)

        return queryset

#http://localhost:8000/api/meals/?suppervision_office_id=1
class MealViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    queryset = Meal.objects.all()
    serializer_class = serializers.MealSerializer

    #query by suppervision office
    def get_queryset(self):
        queryset = self.queryset.filter(isPublish=True)
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')

        if suppervision_office_id!=None:
            suppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)
            queryset = queryset.filter(suppervisionOffice=suppervisionOffice).order_by('price')

        return queryset

#http://localhost:8000/api/supervisionoffices/?area=%E4%B8%AD
class SupervisionOfficeViewSet(viewsets.GenericViewSet,
                                mixins.ListModelMixin,):

    queryset = SupervisionOffice.objects.all()
    serializer_class = (serializers.SupervisionOfficeSerializer)

    def get_queryset(self):
        queryset = self.queryset
        area = self.request.query_params.get('area')

        if area!=None:
            queryset = queryset.filter(area=area)

        return queryset

class OrderViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def get_queryset(self):
        querySet = self.queryset.filter(user=self.request.user).order_by('-id')

        for i in range(len(querySet)):
            querySet[i].supervisionOfficeDetail = querySet[i].supervisionOffice

        return querySet

    def retrieve(self, request, *args, **kwargs):
        order = self.get_object()
        
        order.supervisionOfficeDetail = order.supervisionOffice
        order.products = ProductOrderShip.objects.filter(order=order)
        for i in range(len(order.products)):
            order.products[i].name = order.products[i].product.name
            order.products[i].price = order.products[i].product.price
            order.products[i].subTotal = order.products[i].product.price * order.products[i].amount

        order.outside_products = OutsideProductOrderShip.objects.filter(order=order)
        for i in range(len(order.outside_products)):
            order.outside_products[i].name = order.outside_products[i].outside_product.name
            order.outside_products[i].price = order.outside_products[i].outside_product.price
            order.outside_products[i].subTotal = order.outside_products[i].outside_product.price * order.outside_products[i].amount

        order.meals = MealOrderShip.objects.filter(order=order)
        for i in range(len(order.meals)):
            order.meals[i].name = order.meals[i].meal.name
            order.meals[i].price = order.meals[i].meal.price
            order.meals[i].subTotal = order.meals[i].meal.price * order.meals[i].amount

        serializer = self.get_serializer(order)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user, cashflowState='unPaid')
        config_data = ConfigData.objects.first()
        bank_code = config_data.ATMInfoBankCode
        bank_account = config_data.ATMInfovAccount

        serializer.save(user=self.request.user, cashflowState='waitForATMPay', paymentType='atm', ATMInfoBankCode=bank_code, ATMInfovAccount=bank_account, ATMInfoExpireDate=datetime.now()+timedelta(days=3))

class OrderProductShipViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,):

    queryset = ProductOrderShip.objects.all()
    serializer_class = serializers.ProductOrderShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        order_id = self.request.query_params.get('order_id')
        queryset = queryset.filter(order=Order.objects.get(id=order_id))
        for i in range(len(queryset)):
            queryset[i].name = queryset[i].product.name
            queryset[i].price = queryset[i].product.price
            queryset[i].subTotal = queryset[i].product.price * queryset[i].amount
        return queryset

class OrderOutsideProductShipViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,):

    queryset = OutsideProductOrderShip.objects.all()
    serializer_class = serializers.OutsideProductOrderShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        order_id = self.request.query_params.get('order_id')
        queryset = queryset.filter(order=Order.objects.get(id=order_id))
        for i in range(len(queryset)):
            queryset[i].name = queryset[i].outside_product.name
            queryset[i].price = queryset[i].outside_product.price
            queryset[i].subTotal = queryset[i].outside_product.price * queryset[i].amount
        return queryset

class OrderMealShipViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,):

    queryset = MealOrderShip.objects.all()
    serializer_class = serializers.MealOrderShipSerializer

    def get_queryset(self):
        queryset = self.queryset
        order_id = self.request.query_params.get('order_id')
        queryset = queryset.filter(order=Order.objects.get(id=order_id))
        for i in range(len(queryset)):
            queryset[i].name = queryset[i].product.name
            queryset[i].price = queryset[i].product.price
            queryset[i].subTotal = queryset[i].product.price * queryset[i].amount
        return queryset

#http://localhost:8000/api/search/?q=%E5%8E%9F&suppervision_office_id=1
class SearchViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,):
    
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        queryset = self.queryset
        suppervision_office_id = self.request.query_params.get('suppervision_office_id')
        q = self.request.query_params.get('q')
        
        theSuppervisionOffice = SupervisionOffice.objects.get(id=suppervision_office_id)

        #filter by category
        queryset = queryset.filter(name__contains=q, suppervisionOffice=theSuppervisionOffice)
        

        return queryset

# class ShoppingCartViewSet(viewsets.GenericViewSet,
#                         mixins.ListModelMixin,):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     queryset = ShoppingCart.objects.all()
#     serializer_class = serializers.ShoppingCartSerializer

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)

# class ProductImageViewSet(viewsets.GenericViewSet,
#                             mixins.ListModelMixin,
#                             mixins.RetrieveModelMixin,
#                             mixins.CreateModelMixin,
#                             mixins.UpdateModelMixin):
#     queryset = ProductImage.objects.all()
#     serializer_class = serializers.ProductImageSerializer

#     def get_queryset(self):
#         queryset = self.queryset
#         product_id = self.request.query_params.get('product_id')
#         theProduct = Product.objects.get(id=product_id)
#         queryset = queryset.filter(product=theProduct)
#         return queryset

class AppVersionView(APIView):

    def get(self, request, format=None):

        appVersion = AppVersion.objects.all().order_by('-id').first()

        return Response({'ios': appVersion.iOS_current_version, 'android': appVersion.android_current_version})
    
class AnnouncementViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):
    
    queryset = Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer

    def get_queryset(self):
        queryset = self.queryset.order_by('-create_date')
        return queryset
    
    