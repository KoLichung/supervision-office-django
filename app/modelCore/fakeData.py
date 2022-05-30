import csv
import os
import datetime
from .models import OrderState, ProductOrderShip, User,  Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart
from django.utils import timezone

def importSupervisionOffice():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'county.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if SupervisionOffice.objects.filter(name=row[0]).count()==0:
                supervisionOffice = SupervisionOffice()
                supervisionOffice.name = row[0]
                supervisionOffice.save()
            else:
                supervisionOffice = SupervisionOffice.objects.get(name=row[0])

            

def fakeData():
    def ordermoney(self):
        return self.amount * self.product.price
    user = User()
    user.name = '許小姐'
    user.phone = '0915323131'
    user.email ='happy@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = '周杰倫'
    user.phone = '0985463816'
    user.email = 'cat@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = '蔡英文'
    user.phone = '0985478981'
    user.email = 'president@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User.objects.all()[0]

    category = Category()
    category.name = '會客菜'
    category.save()

    category = Category()
    category.name = '監內百貨商品'
    category.save()

    category = Category()
    category.name = "生活日用品\n(依監所規定)"
    category.save()

    category = Category()
    category.name = "生活用品\n(內衣 內褲 書籍)"
    category.save()

    product = Product()
    product.category = Category.objects.get(id=1)
    product.name = '二小姐 蔓越莓雪Q餅'
    product.price = 165
    product.content = "12 顆 蔓越莓 每顆重量約 18g+-3g 總重約 216g"
    product.info = "1.每顆產品皆是手工現做，注重食材新鮮安全。\n2.不使用化學添加物，減少身體負擔。\n3.用料實在，美味吃得到！經過家人親友長時間的摸索與試吃，研發出合宜的做法，吃起來鬆鬆軟軟，有帶有些微餅乾酥酥脆脆的口感，無法言語形容，只能親口體驗！"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=2)
    product.name = 'SL065_I DO 時尚方型抱枕'
    product.price = 280
    product.content = "材質: 麻、滌綸布"
    product.info = "外觀造型獨特，不失其質感在家的好夥伴，陪你度過悠閒的假期"
    product.save()
    
    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = '小熊餅乾'
    product.price = 280
    product.content = "植物油、小麥粉、砂糖、乳糖、可可塊、澱粉、全脂奶粉、蛋、轉化糖、食鹽、膨脹劑、食用天然色素、香料、乳化劑"
    product.info = "★暢銷多年的好滋味\n★餅乾裡有滿滿的巧克力內餡\n★可愛小熊共有200種圖案"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=4)
    product.name = 'test'
    product.price = 100
    product.content = "test"
    product.info = "test"
    product.save()

    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '台中監理所'
    supervisionOffice.save()

    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '宜蘭監理所'
    supervisionOffice.save()

    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '花蓮監理所'
    supervisionOffice.save()

    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '台南監理所'
    supervisionOffice.save()
    
    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=1)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 2)
    productsupervisionOfficeship.save()

    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=2)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 1)
    productsupervisionOfficeship.save()

    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=3)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 3)
    productsupervisionOfficeship.save()

    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=3)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 4)
    productsupervisionOfficeship.save()

    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=1)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 4)
    productsupervisionOfficeship.save()

    orderstate = OrderState()
    orderstate.name = '未處理'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已完成'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已取消'
    orderstate.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=4)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=2)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=1)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=4)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 4)
    order.supervisionOffice = SupervisionOffice.objects.get(id=2)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=3)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)
    order.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=1)
    productordership.product = Product.objects.get(id=2)
    productordership.amount = 3
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=2)
    productordership.product = Product.objects.get(id=3)
    productordership.amount = 20
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=3)
    productordership.product = Product.objects.get(id=1)
    productordership.amount = 11
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=4)
    productordership.product = Product.objects.get(id=4)
    productordership.amount = 5
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=5)
    productordership.product = Product.objects.get(id=1)
    productordership.amount = 8
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=2)
    productordership.product = Product.objects.get(id=4)
    productordership.amount = 5
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=6)
    productordership.product = Product.objects.get(id=4)
    productordership.amount = 4
    productordership.money = ordermoney(productordership)
    productordership.save()

    payinfo = PayInfo()
    payinfo.order = Order.objects.get(id=1)
    payinfo.save()

    payinfo = PayInfo()
    payinfo.order = Order.objects.get(id=2)
    payinfo.save()

    payinfo = PayInfo()
    payinfo.order = Order.objects.get(id=3)
    payinfo.save()

    shoppingCart = ShoppingCart()
    shoppingCart.user = User.objects.get(id = 2)
    shoppingCart.product = Product.objects.get(id = 1)
    shoppingCart.num = 1
    shoppingCart.save()

    shoppingCart = ShoppingCart()
    shoppingCart.user = User.objects.get(id = 3)
    shoppingCart.product = Product.objects.get(id = 2)
    shoppingCart.num = 2
    shoppingCart.save()