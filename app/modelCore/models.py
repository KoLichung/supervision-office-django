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

def image_upload_handler(instance,filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

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
    objects = UserManager()

    USERNAME_FIELD = 'phone'

class Category(models.Model):
    name = models.CharField(max_length= 100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    
    name = models.CharField(max_length = 255, blank = True, null=True, unique=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    sublabel = models.CharField(max_length = 255, blank = True, null=True,default='')
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    content = models.TextField(default="", blank = True, null=True)
    info = models.TextField(default="", blank = True, null=True)
    unit = models.CharField(max_length = 255, blank = True, null=True,default='')
    stocks = models.IntegerField(default=0, blank = True, null=True)
    week_sum_nums = models.IntegerField(default=0, blank = True, null=True)
    week_sum_revenue = models.IntegerField(default=0, blank = True, null=True)
    
    def __str__(self):
        return self.name

    @property
    def first_image(self):
        return self.images.first()

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'

    )

    image = models.ImageField(upload_to=image_upload_handler, blank=True, null=True)

class SupervisionOffice(models.Model):
    name = models.CharField(max_length = 255, blank = True, null=True)

    def __str__(self):
            return self.name

class ProductSupervisionOfficeShip(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    supervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.CASCADE
    )

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
    orderMoney = models.IntegerField(default=0, null=True)
    prisoner_name = models.CharField(max_length=20, default='', blank = True, null=True)
    prisoner_id = models.CharField(max_length=40, default='', blank = True, null=True)
    memo = models.TextField(default='', null=True, blank=True)

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
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(default=0,null=True)
    money = models.IntegerField(default=0, null=True)

    
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

class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT
    )
    num = models.IntegerField(default=0, blank = True, null=True)