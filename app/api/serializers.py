from rest_framework import serializers
from modelCore.models import Category, Product, SupervisionOffice, Order, ProductOrderShip, Meal, MealOrderShip, AppVersion, OutsideProduct, OutsideProductOrderShip, OutsideCategory, Announcement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)

class OutsideCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OutsideCategory
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id',)

class OutsideProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutsideProduct
        fields = '__all__'
        read_only_fields = ('id',)

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'
        read_only_fields = ('id',)

class SupervisionOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisionOffice
        fields = '__all__'
        read_only_fields = ('id',)


class ProductOrderShipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    subTotal = serializers.IntegerField(read_only=True)

    class Meta:    
        model = ProductOrderShip
        fields = '__all__'
        read_only_fields = ('id',)

class OutsideProductOrderShipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    subTotal = serializers.IntegerField(read_only=True)

    class Meta:    
        model = OutsideProductOrderShip
        fields = '__all__'
        read_only_fields = ('id',)

class MealOrderShipSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    subTotal = serializers.IntegerField(read_only=True)

    class Meta:    
        model = MealOrderShip
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderShipSerializer(read_only=True, many=True)
    outside_products = OutsideProductOrderShipSerializer(read_only=True, many=True)
    meals = MealOrderShipSerializer(read_only=True, many=True)
    supervisionOfficeDetail = SupervisionOfficeSerializer(read_only=True)

    class Meta:    
        model = Order
        fields = '__all__'
        read_only_fields = ('id','user')

class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = '__all__'
        read_only_fields = ('id',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('id',)

