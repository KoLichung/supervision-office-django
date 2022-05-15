from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
import pathlib
import uuid

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not phone:
            raise ValueError('Users must have an phone')
        # user = self.model(email=self.normalize_email(email), **extra_fields)
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

def image_upload_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_fname = str(uuid.uuid1()) #uuid1 -> uuid + timestamp
    return f'images/{new_fname}{fpath.suffix}'

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

    name = models.CharField(max_length = 255, blank = True, null=True)
    price = models.IntegerField(default=0, blank = True, null=True)
    sublabel = models.CharField(max_length = 255, blank = True, null=True,default='')
    isPublish = models.BooleanField(default=True, blank = True, null=True)
    content = models.TextField(default="", blank = True, null=True)
    info = models.TextField(default="", blank = True, null=True)
    unit = models.CharField(max_length = 255, blank = True, null=True,default='')
    stocks = models.IntegerField(default=0, blank = True, null=True)
    

    def __str__(self):
            return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
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
        on_delete=models.RESTRICT
    )
    supervisionOffice = models.ForeignKey(
        SupervisionOffice,
        on_delete=models.RESTRICT
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
        null =True
    )

    #已完成, 未處理, 已取消 
    state =  models.ForeignKey(
        OrderState,
        on_delete=models.RESTRICT,
        null =True
    )

    #paid, failPaid, waitForATMPay, waitForSuperMarketPay  
    cashflowState = models.CharField(max_length=100, default='', blank = True, null=True)

    orderMoney = models.IntegerField(default=0, null=True)
    memo = models.TextField(default='', null=True, blank=True)
    amount = models.IntegerField(default=0,null=True)
    
    isAtm = models.BooleanField(default=False, blank = True, null=True)
    ATMInfoBankCode = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfovAccount = models.CharField(max_length=20, default='', blank = True, null=True)
    ATMInfoExpireDate = models.DateTimeField(auto_now=False, blank = True,null=True)

    createDate = models.DateTimeField(auto_now=False, blank = True,null=True)






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