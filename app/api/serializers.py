from rest_framework import serializers
from modelCore.models import Category , Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip , Order , ShoppingCart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    coverImage = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id','coverImage')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = ('id',)
class SupervisionOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisionOffice
        fields = '__all__'
        read_only_fields = ('id',)

class ProductSuperofficeShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSupervisionOfficeShip
        fields = '__all__'
        read_only_fields = ('id',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Order
        fields = '__all__'
        read_only_fields = ('id',)

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:    
        model = ShoppingCart
        fields = '__all__'
        read_only_fields = ('id',)