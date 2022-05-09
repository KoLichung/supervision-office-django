import csv
import os
from datetime import datetime, timedelta
from .models import User,  Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart


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
    user = User()
    user.name = 'testUser03'
    user.phone = '0915323131'
    user.is_active = True
    user.is_staff =  False
    user.save()

    user = User()
    user.name = 'testUser04'
    user.phone = '0985463816'
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
    
    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '台中監理所'
    supervisionOffice.save()

    supervisionOffice = SupervisionOffice()
    supervisionOffice.name = '宜蘭監理所'
    supervisionOffice.save()
    
    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=1)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 2)
    productsupervisionOfficeship.save()

    productsupervisionOfficeship =ProductSupervisionOfficeShip()
    productsupervisionOfficeship.product = Product.objects.get(id=2)
    productsupervisionOfficeship.supervisionOffice  = SupervisionOffice.objects.get(id = 1)
    productsupervisionOfficeship.save()

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = ProductSupervisionOfficeShip.objects.get(id=1).supervisionOffice
    order.state =  'waitForAtmDeposit'
    order.amount = 5
    order.orderMoney = ProductSupervisionOfficeShip.objects.get(id=1).product.price * order.amount
    order.product = ProductSupervisionOfficeShip.objects.get(id=1).product
    order.save()

    order = Order()
    order.user = User.objects.get(id = 3)
    order.supervisionOffice = ProductSupervisionOfficeShip.objects.get(id=2).supervisionOffice
    order.state =  'waitOwnerCheck'
    order.amount = 3
    order.product = ProductSupervisionOfficeShip.objects.get(id=2).product
    order.orderMoney = ProductSupervisionOfficeShip.objects.get(id=2).product.price * order.amount
    order.save()

    payinfo = PayInfo()
    payinfo.order = Order.objects.get(id=1)
    payinfo.save()

    payinfo = PayInfo()
    payinfo.order = Order.objects.get(id=2)
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