from django.contrib import admin
from .models import  OrderState, ProductOrderShip, User, Category, Product
from .models import  SupervisionOffice, Order, PayInfo, OrderState, Meal, MealOrderShip, AppVersion
from .models import  OutsideProduct, OutsideProductOrderShip, OutsideCategory, ConfigData, Announcement
from .models import SpecialMeal, SpecialMealShip

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')

@admin.register(Category)
class CatogoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name')

@admin.register(OutsideCategory)
class OutsideCatogoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name', 'isPublish', 'category', 'price', 'info')
    list_filter = ['suppervisionOffice','category']

@admin.register(OutsideProduct)
class OutsideProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name', 'isPublish', 'outside_category', 'price', 'info')
    list_filter = ['suppervisionOffice','outside_category']

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'suppervisionOffice', 'name', 'isPublish','price','info')

@admin.register(SupervisionOffice)
class SupervisionOfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'area', 'name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','supervisionOffice','state','orderMoney', 'memo','cashflowState')

@admin.register(ProductOrderShip)
class ProductOrderShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'product' , 'order' ,'amount')

@admin.register(OutsideProductOrderShip)
class OutsideProductOrderShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'outside_product' , 'order' ,'amount')

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

@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ('id','iOS_current_version', 'android_current_version')

@admin.register(ConfigData)
class ConfigDataAdmin(admin.ModelAdmin):
    list_display = ('id','ATMInfoBankCode', 'ATMInfovAccount')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'create_date')

@admin.register(SpecialMeal)
class SpecialMealAdmin(admin.ModelAdmin):
    list_display = ('id','meal','name','isPublish')

@admin.register(SpecialMealShip)
class SpecialMealShipAdmin(admin.ModelAdmin):
    list_display = ('id','order','meal','special_meal','isSpicy','amount')
