from django.contrib import admin
from .models import  OrderState, ProductOrderShip, User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart, OrderState


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')


@admin.register(Category)
class CatogoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category','price','content','info')
    list_filter = ['category']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product' , 'image')

@admin.register(SupervisionOffice)
class SupervisionOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )

@admin.register(ProductSupervisionOfficeShip)
class SupervisionOfficeShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'product' , 'supervisionOffice' )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','supervisionOffice','state','orderMoney', 'memo','cashflowState')

@admin.register(ProductOrderShip)
class ProductOrderShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'product' , 'order' ,'amount','state')

@admin.register(OrderState)
class OrderState(admin.ModelAdmin):
    list_display=('id','name')


@admin.register(PayInfo)
class PayInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order' , 'PaymentType' )

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user' , 'product','num' )