from itertools import product
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
import pathlib
import uuid
from django.db.models import Sum 

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        user = self.model(
            phone = phone, 
            name=extra_fields.get('name'),
            line_user_id=extra_fields.get('line_user_id'),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password, **extra_fields):
        """Creates and saves a new super user"""
        user = self.create_user(phone, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

# def image_upload_handler(instance,filename):
#     fpath = pathlib.Path(filename)
#     new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
#     return f'images/{new_fname}{fpath.suffix}'

@property
def get_photo_url(self):
    if self.photo and hasattr(self.photo, 'url'):
        return self.photo.url
    else:
        return "/static/backboard/assets/img/generic/4.jpg"
         
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    phone = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255, null=True , blank=True)
    email = models.CharField(max_length=255, null=True , blank=True,default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    line_id = models.CharField(max_length=255, null=True , blank=True)
    line_user_id = models.CharField(max_length=255, null=True , blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

class SupervisionOffice(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)
    # 北中南東
    area = models.CharField(max_length = 20, blank = True, null=True)
    def __str__(self):
            return self.name

class Category(models.Model):
    name = models.CharField(max_length= 100)
    suppervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class OutsideCategory(models.Model):
    name = models.CharField(max_length= 100)
    suppervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    suppervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE
    )
    
    code = models.CharField(max_length = 100, blank = True, null=True)
    name = models.CharField(max_length = 255, blank = True, null=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    info = models.TextField(default="", blank = True, null=True)
    unit = models.CharField(max_length = 255, blank = True, null=True,default='')
    stocks = models.IntegerField(default=0, blank = True, null=True)
    week_sum_nums = models.IntegerField(default=0, blank = True, null=True)
    week_sum_revenue = models.IntegerField(default=0, blank = True, null=True)
    # content = models.TextField(default="", blank = True, null=True)
    # sublabel = models.CharField(max_length = 255, blank = True, null=True,default='')

    def __str__(self):
        return self.name

    # @property
    # def first_image(self):
    #     return self.images.first()
class OutsideProduct(models.Model):
    outside_category = models.ForeignKey(
        OutsideCategory,
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
    )
    suppervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE
    )
    
    code = models.CharField(max_length = 100, blank = True, null=True)
    name = models.CharField(max_length = 255, blank = True, null=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    info = models.TextField(default="", blank = True, null=True)
    unit = models.CharField(max_length = 255, blank = True, null=True,default='')
    stocks = models.IntegerField(default=0, blank = True, null=True)
    week_sum_nums = models.IntegerField(default=0, blank = True, null=True)
    week_sum_revenue = models.IntegerField(default=0, blank = True, null=True)
    # content = models.TextField(default="", blank = True, null=True)
    # sublabel = models.CharField(max_length = 255, blank = True, null=True,default='')

    def __str__(self):
        return self.name
# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='images'

#     )

#     image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

class Meal(models.Model):
    suppervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE,
        related_name='meal',
    )
    
    code = models.CharField(max_length = 100, blank = True, null=True)
    name = models.CharField(max_length = 255, blank = True, null=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    info = models.TextField(default="", blank = True, null=True)
    unit = models.CharField(max_length = 255, blank = True, null=True,default='')
    stocks = models.IntegerField(default=0, blank = True, null=True)
    week_sum_nums = models.IntegerField(default=0, blank = True, null=True)
    week_sum_revenue = models.IntegerField(default=0, blank = True, null=True)

    def __str__(self):
        return self.name
    
# class ProductSupervisionOfficeShip(models.Model):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE
#     )
#     supervisionOffice = models.ForeignKey(
#         SupervisionOffice,
#         on_delete=models.CASCADE
#     )

class OrderState(models.Model):
    name = models.CharField(max_length=255, null=True , blank=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )
    supervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.RESTRICT,
        null=True
    )
    #已完成, 未處理, 已取消 
    state =  models.ForeignKey(
        OrderState,
        on_delete=models.RESTRICT,
        null =True
    )
    #unPaid, paid, failPaid, waitForATMPay, waitForCVSPay  
    cashflowState = models.CharField(max_length=100, default='', blank = True, null=True)

    ship_fee = models.IntegerField(default=0, null=True)
    petty_cash = models.IntegerField(default=0, null=True)

    orderMoney = models.IntegerField(default=0, null=True)
    prisoner_name = models.CharField(max_length=20, default='', blank = True, null=True)
    prisoner_id = models.CharField(max_length=40, default='', blank = True, null=True)
    memo = models.TextField(default='', null=True, blank=True)
    sender_name = models.CharField(max_length=20, default='', blank = True, null=True)

    is_urgent = models.BooleanField(default=False)

    #credit, atm, cvs
    paymentType = models.CharField(max_length=20, default='', blank = True, null=True)

    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoExpireDate = models.DateTimeField(auto_now=False, blank = True,null=True)
    ATMFiveDigit = models.CharField(max_length=20, default='', blank = True, null=True)

    CVSInfoPaymentNo = models.CharField(max_length=20, default='', blank = True, null=True)
    CVSInfoPaymentURL = models.CharField(max_length=100, default='', blank = True, null=True)
    CVSInfoExpireDate = models.DateTimeField(auto_now_add=False, blank = True,null=True)

    createDate = models.DateTimeField(auto_now=False, blank = True,null=True)

class ProductOrderShip(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        blank = True,
        null=True,
    )
    amount = models.IntegerField(default=0,null=True)
    money = models.IntegerField(default=0, null=True)

class OutsideProductOrderShip(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    outside_product = models.ForeignKey(
        OutsideProduct,
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(default=0,null=True)
    money = models.IntegerField(default=0, null=True)

class MealOrderShip(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    meal = models.ForeignKey(
        Meal,
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(default=0,null=True)
    money = models.IntegerField(default=0, null=True)

# class PettyCash(models.Model):
#     order = models.ForeignKey(
#         Order,
#         on_delete=models.RESTRICT
#     )
#     user = models.ForeignKey(
#         User,
#         null=True,
#         on_delete=models.SET_NULL
#     )
#     money = models.IntegerField(default=0, null=True,  blank = True)

class MtPayInfo(models.Model):
    # 目前是超商代收 only
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )

    #付款代碼
    payment_number = models.CharField(max_length=100, default='', blank = True, null=True)

    # 訂單號
    number = models.CharField(max_length=100, default='', blank = True, null=True)
    # 訂單金額
    amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)


    STATUS_CHOICES = [
        (1, '已建立'),
        (2, '已付款'),
        (3, '已取消'),
        (4, '已打單'),
        (5, '已付款，但實際付款金額與訂單金額不符'),
        (6, '已付款，但付款銀行資訊不符'),
        (7, '已退款，付款銀行資訊不符'),
    ]
    # 交易狀態
    status = models.IntegerField(default=1, choices=STATUS_CHOICES,null=True)
    #超商繳費時限
    query_limit_at = models.DateTimeField(auto_now=False, blank = True, null=True)

    # 繳費時間
    pay_at = models.DateTimeField(auto_now=False, blank = True, null=True)
    # 繳費金額
    pay_amount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    # 加密類型
    encrypt_type = models.IntegerField(default=0, null=True)
    # 繳費方式
    payment_method_id = models.IntegerField(default=0, null=True)
    # 銀行虛擬帳號
    virtual_bank_id  = models.IntegerField(default=0, null=True)
    # 客戶訂單號
    customer_number = models.CharField(max_length=100, default='', blank = True, null=True)
    # 加密簽章
    sign = models.CharField(max_length=100, default='', blank = True, null=True)
    # 繳費記錄
    payment_records = models.CharField(max_length=255, default='', blank = True, null=True)

class PayInfo(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.RESTRICT
    )
    
    PaymentType = models.CharField(max_length=100, default='', blank = True, null=True)
    MerchantID = models.CharField(max_length=100, default='', blank = True, null=True)
    
    OrderInfoMerchantTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeDate = models.DateTimeField(auto_now=False,null=True)
    OrderInfoTradeNo = models.CharField(max_length=100, default='', blank = True, null=True)
    OrderInfoTradeAmt = models.IntegerField(default=0, null=True)
    OrderInfoPaymentType = models.CharField(max_length=20, default='', blank = True, null=True)
    OrderInfoChargeFee = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    OrderInfoTradeStatus = models.CharField(max_length=20, default='', blank = True, null=True)

    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoExpireDate = models.DateTimeField(auto_now=False,null=True)

    CVSInfoPayFrom = models.CharField(max_length=20, default='', blank = True, null=True)
    CVSInfoPaymentNo = models.CharField(max_length=20, default='', blank = True, null=True)
    CVSInfoPaymentURL = models.CharField(max_length=100, default='', blank = True, null=True)

    CardInfoAuthCode = models.CharField(max_length=100, default='', blank = True, null=True)
    CardInfoGwsr = models.IntegerField(default=0, null=True)
    CardInfoProcessDate =  models.DateTimeField(auto_now=False,null=True)
    CardInfoAmount = models.IntegerField(default=0, null=True)
    CardInfoCard6No = models.CharField(max_length=20, default='', blank = True, null=True)
    CardInfoCard4No = models.CharField(max_length=20, default='', blank = True, null=True)

# class ShoppingCart(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.RESTRICT
#     )
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.RESTRICT
#     )
#     num = models.IntegerField(default=0, blank = True, null=True)

class AppVersion(models.Model):
    iOS_current_version = models.CharField(max_length=10, default='', blank = True, null=True)
    android_current_version = models.CharField(max_length=10, default='', blank = True, null=True)

class ConfigData(models.Model):
    ATMInfoBankCode = models.CharField(max_length=10, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=35, default='', blank = True, null=True)

class Announcement(models.Model):
    content = models.TextField(default='', blank = True, null=True)
    create_date = models.DateTimeField(auto_now=False,null=True)

class SpecialMeal(models.Model):
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
    )
    code = models.CharField(max_length = 100, blank = True, null=True)
    name = models.CharField(max_length = 255, blank = True, null=True)
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    
    def __str__(self):
        return self.name

class SpecialMealShip(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    meal = models.ForeignKey(
        Meal,
        on_delete=models.CASCADE,
    )
    special_meal = models.ForeignKey(
        SpecialMeal,
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(default=0,null=True)
    money = models.IntegerField(default=0, null=True)
    isSpicy = models.BooleanField(default=False, blank = True, null=True)