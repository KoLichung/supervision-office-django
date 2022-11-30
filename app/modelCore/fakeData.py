import csv
import os
import datetime 
from datetime import timedelta
from .models import OrderState, ProductOrderShip, User,  Category, Product, SupervisionOffice, Order ,PayInfo, Meal
from django.utils import timezone

def set_sand_box_data():
    importSupervisionOffice()
    seedData()
    fakeData()

def importSupervisionOffice():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'supervision_office.csv')

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if SupervisionOffice.objects.filter(name=row[0]).count()==0:
                supervisionOffice = SupervisionOffice()
                supervisionOffice.name = row[0].replace('法務部矯正署','').replace('臺','台')
                supervisionOffice.area = row[3]
                supervisionOffice.save()
            else:
                supervisionOffice = SupervisionOffice.objects.get(name=row[0])

def seedData():
    # category = Category()
    # category.name = '會客菜'
    # category.save()

    # category = Category()
    # category.name = '監內百貨商品'
    # category.save()

    # category = Category()
    # category.name = "生活日用品\n(依監所規定)"
    # category.save()
            
    orderstate = OrderState()
    orderstate.name = '未處理'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已完成'
    orderstate.save()

    orderstate = OrderState()
    orderstate.name = '已取消'
    orderstate.save()

def importProduct():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'taipei_products.csv')
    
    suppervisionOffice = SupervisionOffice.objects.get(id=1)

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if Product.objects.filter(name=row[1],suppervisionOffice=suppervisionOffice).count()==0:
                product = Product()
                product.suppervisionOffice = suppervisionOffice
                product.code = row[0]
                product.name = row[1]

                if Category.objects.filter(name=row[2],suppervisionOffice=suppervisionOffice).count()==0:
                    category = Category.objects.create(name=row[2],suppervisionOffice=suppervisionOffice)
                else:
                    category = Category.objects.filter(name=row[2],suppervisionOffice=suppervisionOffice).first()

                product.category = category
                product.unit = row[3]
                product.price = int(row[4])
                product.info = row[5]
                product.save()

def importMeal():
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'taipei_meals.csv')
    
    suppervisionOffice = SupervisionOffice.objects.get(id=1)

    file = open(file_path)
    reader = csv.reader(file, delimiter=',')
    for index, row in enumerate(reader):
        if index != 0:
            if Meal.objects.filter(name=row[1],suppervisionOffice=suppervisionOffice).count()==0:
                meal = Meal()
                meal.suppervisionOffice = suppervisionOffice
                meal.code = row[0]
                meal.name = row[1]
                meal.unit = row[2]
                meal.price = int(row[3])
                meal.info = row[4]
                meal.save()


def fakeData():
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

    user = User()
    user.name = 'test01'
    user.phone = '0980178981'
    user.email = 'test01@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test02'
    user.phone = '0989078981'
    user.email = 'test02@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test03'
    user.phone = '0985472481'
    user.email = 'test03@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test04'
    user.phone = '0985470481'
    user.email = 'president04@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test05'
    user.phone = '0980578981'
    user.email = 'president05@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test06'
    user.phone = '0985478061'
    user.email = 'president06@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test07'
    user.phone = '0985470071'
    user.email = 'president07@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test08'
    user.phone = '0985478991'
    user.email = 'president08@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'test09'
    user.phone = '0985478091'
    user.email = 'president09@gmail.com'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User.objects.all()[0]

    product = Product()
    product.category = Category.objects.get(id=1)
    product.name = '二小姐 蔓越莓雪Q餅'
    product.price = 165
    product.info = "1.每顆產品皆是手工現做，注重食材新鮮安全。\n2.不使用化學添加物，減少身體負擔。\n3.用料實在，美味吃得到！經過家人親友長時間的摸索與試吃，研發出合宜的做法，吃起來鬆鬆軟軟，有帶有些微餅乾酥酥脆脆的口感，無法言語形容，只能親口體驗！"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=2)
    product.name = 'SL065_I DO 時尚方型抱枕'
    product.price = 280
    product.info = "外觀造型獨特，不失其質感在家的好夥伴，陪你度過悠閒的假期"
    product.save()
    
    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = '小熊餅乾'
    product.price = 280
    product.info = "★暢銷多年的好滋味\n★餅乾裡有滿滿的巧克力內餡\n★可愛小熊共有200種圖案"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = 'test01'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = 'test02'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = 'test03'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = 'test04'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=2)
    product.name = 'test05'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=1)
    product.name = 'test06'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=2)
    product.name = 'test07'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=3)
    product.name = 'test08'
    product.price = 100
    product.info = "test"
    product.save()

    product = Product()
    product.category = Category.objects.get(id=2)
    product.name = 'test09'
    product.price = 100
    product.info = "test"
    product.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=7)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=2)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=2)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=1)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=3)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=4)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=1)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 4)
    order.supervisionOffice = SupervisionOffice.objects.get(id=2)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=3)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=3)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=4)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 7)
    order.supervisionOffice = SupervisionOffice.objects.get(id=9)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=2)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=8)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=3)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 8)
    order.supervisionOffice = SupervisionOffice.objects.get(id=2)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=4)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 9)
    order.supervisionOffice = SupervisionOffice.objects.get(id=1)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=3)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 5)
    order.supervisionOffice = SupervisionOffice.objects.get(id=7)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=2)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=5)
    order.state =  OrderState.objects.get(id=2)
    order.createDate = datetime.datetime.now(tz=timezone.utc)- timedelta(days=5)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=7)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = SupervisionOffice.objects.get(id=9)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=3)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 7)
    order.supervisionOffice = SupervisionOffice.objects.get(id=7)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=7)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 12)
    order.supervisionOffice = SupervisionOffice.objects.get(id=11)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=100)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 8)
    order.supervisionOffice = SupervisionOffice.objects.get(id=8)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=8)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 6)
    order.supervisionOffice = SupervisionOffice.objects.get(id=7)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 9)
    order.supervisionOffice = SupervisionOffice.objects.get(id=4)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 11)
    order.supervisionOffice = SupervisionOffice.objects.get(id=9)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=2)
    order.save()

    order = Order()
    order.user = User.objects.get(id = 10)
    order.supervisionOffice = SupervisionOffice.objects.get(id=10)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
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

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=7)
    productordership.product = Product.objects.get(id=8)
    productordership.amount = 40
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=8)
    productordership.product = Product.objects.get(id=7)
    productordership.amount = 25
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=9)
    productordership.product = Product.objects.get(id=3)
    productordership.amount = 7
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=10)
    productordership.product = Product.objects.get(id=9)
    productordership.amount = 19
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=11)
    productordership.product = Product.objects.get(id=10)
    productordership.amount = 30
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=12)
    productordership.product = Product.objects.get(id=6)
    productordership.amount = 10
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=7)
    productordership.product = Product.objects.get(id=7)
    productordership.amount = 7
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=13)
    productordership.product = Product.objects.get(id=12)
    productordership.amount = 33
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=14)
    productordership.product = Product.objects.get(id=7)
    productordership.amount = 3
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=15)
    productordership.product = Product.objects.get(id=7)
    productordership.amount = 31
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=16)
    productordership.product = Product.objects.get(id=8)
    productordership.amount = 5
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=17)
    productordership.product = Product.objects.get(id=1)
    productordership.amount = 9
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=18)
    productordership.product = Product.objects.get(id=10)
    productordership.amount = 13
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=19)
    productordership.product = Product.objects.get(id=2)
    productordership.amount = 2
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=20)
    productordership.product = Product.objects.get(id=9)
    productordership.amount = 11
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=21)
    productordership.product = Product.objects.get(id=8)
    productordership.amount = 20
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=16)
    productordership.product = Product.objects.get(id=5)
    productordership.amount = 5
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = Order.objects.get(id=21)
    productordership.product = Product.objects.get(id=9)
    productordership.amount = 14
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

def ordermoney(self):
    return self.amount * self.product.price