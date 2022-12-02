from django.contrib import admin
from .models import  OrderState, ProductOrderShip, User, Category, Product, SupervisionOffice, Order, PayInfo, OrderState, Meal, MealOrderShip


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

@admin.register(Category)
class CatogoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name', 'category','price','info')
    list_filter = ['category']

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name','price','info')

@admin.register(SupervisionOffice)
class SupervisionOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'area', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','supervisionOffice','state','orderMoney', 'memo','cashflowState')

@admin.register(ProductOrderShip)
class ProductOrderShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'product' , 'order' ,'amount')

@admin.register(MealOrderShip)
class MealOrderShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal' , 'order' ,'amount')

# @admin.register(PettyCash)
# class PettyCashAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order' , 'user' ,'money')

@admin.register(OrderState)
class OrderState(admin.ModelAdmin):
    list_display=('id','name')

@admin.register(PayInfo)
class PayInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order' , 'PaymentType' )
