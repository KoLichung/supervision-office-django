import csv
import os
import datetime 
from datetime import timedelta
from .models import OrderState, ProductOrderShip, User,  Category, Product, SupervisionOffice, Order ,PayInfo, Meal, MealOrderShip
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

    order = Order()
    order.user = User.objects.get(id = 2)
    order.supervisionOffice = SupervisionOffice.objects.get(id=1)
    order.state =  OrderState.objects.get(id=1)
    order.createDate = datetime.datetime.now(tz=timezone.utc) - timedelta(days=1)
    order.ship_fee = 200
    order.petty_cash = 300
    order.save()

    productordership = ProductOrderShip()
    productordership.order = order
    productordership.product = Product.objects.get(id=1)
    productordership.amount = 3
    productordership.money = ordermoney(productordership)
    productordership.save()

    productordership = ProductOrderShip()
    productordership.order = order
    productordership.product = Product.objects.get(id=2)
    productordership.amount = 2
    productordership.money = ordermoney(productordership)
    productordership.save()

    mealOrderShip = MealOrderShip()
    mealOrderShip.order = order
    mealOrderShip.meal = Meal.objects.get(id=1)
    mealOrderShip.amount = 2
    # mealOrderShip.money = ordermoney(mealOrderShip)
    mealOrderShip.save()


def ordermoney(self):
    return self.amount * self.product.price