from calendar import month
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from modelCore.models import User , Category, Product, SupervisionOffice, Order ,ProductOrderShip, PayInfo, OrderState, Meal, MealOrderShip, OutsideProduct, OutsideCategory, OutsideProductOrderShip
# from modelCore.forms import *
import urllib 
from django.db.models import Sum
from datetime import datetime, timedelta
from django.contrib import auth
from django.contrib.auth import authenticate
import csv
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

# Create your views here.
def login(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/backboard/orders')
        else:
            return redirect('/backboard/')

    return render(request, 'backboard/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/backboard/')

# def index(request):
#     if not request.user.is_authenticated or not request.user.is_staff:
#         return redirect('/backboard/')

#     orders = Order.objects.filter(state=1)
#     ships = ProductOrderShip.objects.all()
#     products =Product.objects.all()
#     undealtorders = Order.objects.filter(state=1)
#     UndealtOrdersNum = undealtorders.count()
#     dealtOrdersShips = Order.objects.filter(state=2)
#     last7Days = (datetime.today() - timedelta(days=7)).date()
#     last6Days = (datetime.today() - timedelta(days=6)).date()
#     last5Days = (datetime.today() - timedelta(days=5)).date()
#     last4Days = (datetime.today() - timedelta(days=4)).date()
#     last3Days = (datetime.today() - timedelta(days=3)).date()
#     last2Days = (datetime.today() - timedelta(days=2)).date()
#     last1Days = (datetime.today() - timedelta(days=1)).date()
#     WeekOrders = dealtOrdersShips.filter(createDate__date__gte=last7Days)
#     last7DaysOrders = dealtOrdersShips.filter(createDate__date=last7Days)
#     last6DaysOrders = dealtOrdersShips.filter(createDate__date=last6Days)
#     last5DaysOrders = dealtOrdersShips.filter(createDate__date=last5Days)
#     last4DaysOrders = dealtOrdersShips.filter(createDate__date=last4Days)
#     last3DaysOrders = dealtOrdersShips.filter(createDate__date=last3Days)
#     last2DaysOrders = dealtOrdersShips.filter(createDate__date=last2Days)
#     last1DaysOrders = dealtOrdersShips.filter(createDate__date=last1Days)
#     sum7=0
#     sum6=0
#     sum5=0
#     sum4=0
#     sum3=0
#     sum2=0
#     sum1=0
#     sum7Money=0 
#     sum6Money=0
#     sum5Money=0
#     sum4Money=0
#     sum3Money=0
#     sum2Money=0
#     sum1Money=0
#     for last7DaysOrder in last7DaysOrders:
#         ships7 = ships.filter(order=last7DaysOrder)
#         for ship in ships7:
#             sum7 += ship.amount
#             sum7Money += ship.product.price * ship.amount
#     for last6DaysOrder in last6DaysOrders:
#         ships6 = ships.filter(order=last6DaysOrder)
#         for ship in ships6:
#             sum6 += ship.amount
#             sum6Money += ship.product.price * ship.amount
#     for last5DaysOrder in last5DaysOrders:
#         ships5 = ships.filter(order=last5DaysOrder)
#         for ship in ships5:
#             sum5 += ship.amount
#             sum5Money += ship.product.price * ship.amount
#     for last4DaysOrder in last4DaysOrders:
#         ships4 = ships.filter(order=last4DaysOrder)
#         for ship in ships4:
#             sum4 += ship.amount
#             sum4Money += ship.product.price * ship.amount
#     for last3DaysOrder in last3DaysOrders:
#         ships3 = ships.filter(order=last3DaysOrder)
#         for ship in ships3:
#             sum3 += ship.amount
#             sum3Money += ship.product.price * ship.amount
#     for last2DaysOrder in last2DaysOrders:
#         ships2 = ships.filter(order=last2DaysOrder)
#         for ship in ships2:
#             sum2 += ship.amount
#             sum2Money += ship.product.price * ship.amount
#     for last1DaysOrder in last1DaysOrders:
#         ships1 = ships.filter(order=last1DaysOrder)
#         for ship in ships1:
#             sum1 += ship.amount
#             sum1Money += ship.product.price * ship.amount
#     for product in products:
#         sum = 0
#         for WeekOrder in WeekOrders:
#             OrderShips=ships.filter(order=WeekOrder,product=product)       
#             for OrderShip in OrderShips:
#                 sum += OrderShip.amount                 
#         product.week_sum_nums = sum      
#         product.save()   
#     sumtotal= sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7
#     sumTotalMoney = sum1Money +sum2Money + sum3Money +sum4Money + sum5Money+ sum6Money + sum7Money
#     forlooplist = []
#     last10Orders = orders.order_by('-createDate')[:10]
#     for order in last10Orders:
#         sum = 0
#         TotalMoney = ships.filter(order=order).aggregate(Sum('money'))
#         if TotalMoney['money__sum'] != None:
#             sum += TotalMoney['money__sum']
#             forlooplist.append({'sum':sum,'order':order})
    
#     productRank = Product.objects.order_by("-week_sum_nums")[:3]
    
#     return render(request, 'backboard/index.html',{'sumTotalMoney':sumTotalMoney, 'sumtotal':sumtotal, 'forlooplist':forlooplist, 'sum7Money':sum7Money,'sum6Money':sum6Money,'sum5Money':sum5Money,'sum4Money':sum4Money,'sum3Money':sum3Money,'sum2Money':sum2Money,'sum1Money':sum1Money, 'sum1':sum1,'sum2':sum2,'sum3':sum3,'sum4':sum4,'sum5':sum5,'sum6':sum6,'sum7':sum7, 'last6Days':last6Days,'last5Days':last5Days,'last4Days':last4Days ,'last3Days':last3Days,'last2Days':last2Days,'last1Days':last1Days, 'last7Days':last7Days, 'orders':orders,'UndealtOrdersNum':UndealtOrdersNum,'productRank':productRank})

def bills(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    offices = SupervisionOffice.objects.all()
    orders=Order.objects.filter(state=2)
     
    ships = ProductOrderShip.objects.all()
  
    
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    this_month = Order.objects.filter(createDate__year=current_year,
                           createDate__month=current_month)
    
    monthId = request.GET.get('lastMonth')
    if current_month-int(monthId) > 0:
        month_id = current_month - int(monthId)
        yearId = current_year
        
    elif current_month-int(monthId) <= 0:
        month_id = current_month - int(monthId) + 12
        yearId = current_year-1
        
    dict_office = {}
    dict_all = {}
    listMonth = {}
    listYear = {}
    for i in range(6):
        theMonth = current_month -i
        if theMonth > 0:
            month = theMonth
            year = current_year
        else:
            month = theMonth + 12
            year = current_year - 1
        dict_all['last'+str(i)+'Months'] = orders.filter(createDate__year=year,
                           createDate__month=month)
        for x in range(1,offices.count()+1):
            officeOrders =  orders.filter(supervisionOffice=x) 
            dict_office['last'+str(i)+'Months'+'office_id'+str(x)] = officeOrders.filter(createDate__year=year,
                            createDate__month=month)
            
        listMonth['last'+str(i)+'Month'] = month
        listYear['last'+str(i)+'Month'] = year
    sum = 0
    if dict_all['last'+str(monthId)+'Months'] != None:
        TotalOrder = dict_all['last'+str(monthId)+'Months'].count()
        for order in dict_all['last'+str(monthId)+'Months']:
            TotalMoney = ships.filter(order=order).aggregate(Sum('money'))
            if TotalMoney['money__sum'] != None:
                sum += TotalMoney['money__sum']
        
    else:
        TotalOrder = 0

    officeTotalMoney = {}
    officeTotalorder = {}
    forlooplist=[] 
    for x in range(1,offices.count()+1):
        
        officeTotalMoney['office_id_'+str(x)] = 0
        if dict_office['last'+str(monthId)+'Months'+'office_id'+str(x)] != None:
            officeTotalorder['office_id_'+str(x)] = dict_office['last'+str(monthId)+'Months'+'office_id'+str(x)].count()
            for officeOrder in dict_office['last'+str(monthId)+'Months'+'office_id'+str(x)]:
                TotalMoney = ships.filter(order=officeOrder).aggregate(Sum('money'))
                if TotalMoney['money__sum'] != None:
                        officeTotalMoney['office_id_'+str(x)] += TotalMoney['money__sum']
            
        else:
            officeTotalorder['office_id_'+str(x)] = 0
        forlooplist.append({'office':offices.get(id=x) ,'Totalorder':officeTotalorder['office_id_'+str(x)],'TotalMoney':officeTotalMoney['office_id_'+str(x)]})
    

    paginator = Paginator(forlooplist, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)
    if request.method == 'POST':
        
        checkMonth = request.POST.get('selectMonth')
        your_params = {
        'lastMonth': checkMonth
    }
        return redirect_params('bills', your_params)

    return render(request, 'backboard/bills.html',{'sum':sum, 'forlooplist':page_obj, 'monthId':monthId, 'listMonth':listMonth,'listYear':listYear, 'month_id':month_id,'yearId':yearId, 'current_month':current_month,'current_year':current_year, 'dict_all':dict_all,'this_month':this_month,'offices':offices, 'TotalOrder':TotalOrder,'officeTotalorder':officeTotalorder,'officeTotalMoney':officeTotalMoney})

def customers(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    customers = User.objects.all().order_by('-id')

    paginator = Paginator(customers, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/customers.html',{'customers':page_obj})

def customer_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    # customers = User.objects.all()
    orders = Order.objects.all()
    customer_id = request.GET.get('customer_id')
    customer = User.objects.get(id=customer_id)

    if request.method == 'POST' and 'reset_password' in request.POST :
        password = "12345"
        customer.set_password(password)
        customer.save()

    ships = ProductOrderShip.objects.all()
    forlooplist=[] 
    for order in orders:
        sum = 0
        if order.user == customer:
            TotalMoney = ships.filter(order=order).aggregate(Sum('money'))
            if TotalMoney['money__sum'] != None:
                sum += TotalMoney['money__sum']
                forlooplist.append({'user':order.user ,'sum':sum,'order':order})

    return render(request, 'backboard/customer_detail.html',{'forlooplist':forlooplist, 'orders':orders,'customer':customer})

def orders(request):    
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    orders = Order.objects.all().order_by('-id')
    orderstates = OrderState.objects.all()

    order_state_id = request.GET.get('order_state')
    if order_state_id != None and order_state_id != "None":
        theOrderstate = orderstates.get(id=order_state_id)      
        theOrders = orders.filter(state=theOrderstate)  
    else:
        theOrders = orders

    paginator = Paginator(theOrders, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/orders.html',{'q':order_state_id ,'orders':page_obj,'orderstates':orderstates})
    
def order_detail(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    order_id=request.GET.get('IdOrder')
    order = Order.objects.get(id=order_id)        
    ships = ProductOrderShip.objects.filter(order=order)
    outsideProductShips = OutsideProductOrderShip.objects.filter(order=order)
    mealShips = MealOrderShip.objects.filter(order=order)
    orderstates = OrderState.objects.all()

    if request.method == 'POST':
        if request.POST.get('OrderState') != None:
            state_Id = request.POST.get('OrderState')
            order.state = OrderState.objects.get(id=state_Id)
        if request.POST.get('cashflow_state') != None:
            order.cashflowState = request.POST.get('cashflow_state')
        order.save()
        return redirect(f'/backboard/order_detail?IdOrder={order_id}')

    return render(request, 'backboard/order_detail.html',{'order':order, 'ships':ships, 'outsideProductShips':outsideProductShips,'mealShips':mealShips, 'orderstates':orderstates})

def offices_order(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    offices_all = SupervisionOffice.objects.all()
    ships = ProductOrderShip.objects.all()
    office_Id = request.GET.get('OfficeId')
    monthId = request.GET.get('lastMonth')
    orders =  Order.objects.filter(supervisionOffice=office_Id,state=2)
    theOffice = offices_all.get(id=office_Id)
    today = datetime.today()
    current_month = today.month
    current_year = today.year
       
    if current_month-int(monthId) > 0:
        month = current_month - int(monthId)
        year = current_year
        
    elif current_month-int(monthId) <= 0:
        month = current_month - int(monthId) + 12
        year = current_year-1
        
    currentOrders = orders.filter(createDate__year=year,createDate__month=month)
    looplist=[]
    sum = 0
    for order in currentOrders:
        for ship in ships:
            if ship.order==order:
                sum += ship.amount * ship.product.price
                looplist.append({'name':ship.product.name,'price':ship.product.price,'amount':ship.amount,'ordermoney':ship.product.price * ship.amount})

    return render(request,'' 'backboard/offices_order.html',{'looplist':looplist, 'currentOrders':currentOrders, 'ships':ships,'orders':orders,'theOffice':theOffice,'sum':sum})


def products(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    

    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    # 匯入
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        file = open(file_path)
        reader = csv.reader(file, delimiter=',')
        for index, row in enumerate(reader):
            if index != 0:
                if Product.objects.filter(name=row[1],suppervisionOffice=supervisionOffice).count()==0:
                    product = Product()
                    product.suppervisionOffice = supervisionOffice
                    product.code = row[0]
                    product.name = row[1]

                    if Category.objects.filter(name=row[2],suppervisionOffice=supervisionOffice).count()==0:
                        category = Category.objects.create(name=row[2],suppervisionOffice=supervisionOffice)
                    else:
                        category = Category.objects.filter(name=row[2],suppervisionOffice=supervisionOffice).first()

                    product.category = category
                    product.unit = row[3]
                    product.price = int(row[4])
                    product.info = row[5]
                    product.save()
        return redirect(f'/backboard/products?supervisionOfficeId={supervisionOfficeId}')

    
    supervisionOffices = SupervisionOffice.objects.all()
    products = Product.objects.all().order_by('-id')
    
    # print(supervisionOffices)
    products = products.filter(suppervisionOffice=supervisionOffice)

    
    paginator = Paginator(products, 50)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    # page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/products.html',{'supervisionOffices':supervisionOffices, 'supervisionOfficeId':supervisionOfficeId, 'products':page_obj})

def add_new_product(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    categories = Category.objects.filter(suppervisionOffice=supervisionOffice)
 
    if request.method == 'POST':
            supervisionOfficeId = request.POST.get('supervisionOfficeId')
            supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

            product = Product()
            product.suppervisionOffice = supervisionOffice
            product.code = request.POST.get('productCode')
            product.name = request.POST.get('productName') 
            category_Id = request.POST.get('productCategory')
            product.category = Category.objects.get(id=category_Id)
            product.info = request.POST.get('productInfo')
            product.price = request.POST.get('productPrice')
            if request.POST.get('productUnit') != None:
                product.unit =request.POST.get('productUnit')
            if request.POST.get('productStock') != None:
                product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
        
            return redirect_params('products',{'supervisionOfficeId':product.suppervisionOffice.id})
    
    return render(request, 'backboard/add_new_product.html',{'categories':categories, 'supervisionOfficeId':supervisionOfficeId})
         
def edit_product(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    productId = request.GET.get("productId")
    theProduct = Product.objects.get(id=productId)

    supervisionOffice = theProduct.suppervisionOffice
    categories = Category.objects.filter(suppervisionOffice=supervisionOffice)
    
    if request.method == 'POST':

        # not related to image
        product = Product.objects.get(id=productId)
        product.code = request.POST.get('productCode')
        product.name = request.POST.get('productName')
        category_Id = request.POST.get('productCategory')
        product.category = Category.objects.get(id=category_Id)
        product.info = request.POST.get('productInfo')
        product.price = request.POST.get('productPrice')
        product.unit =request.POST.get('productUnit')
        product.stocks = request.POST.get('productStock')
        product.isPublish = request.POST.get('productIspublish')
        product.save()
                    
        # return redirect_params('edit_product',{'productId':productId})

        return redirect_params('products',{'supervisionOfficeId':product.suppervisionOffice.id})
        
    
    return render(request, 'backboard/edit_product.html',{'categories':categories,'productId':productId,'product':theProduct})


def outside_products(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    

    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    # 匯入
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        file = open(file_path)
        reader = csv.reader(file, delimiter=',')
        for index, row in enumerate(reader):
            if index != 0:
                if OutsideProduct.objects.filter(name=row[1],suppervisionOffice=supervisionOffice).count()==0:
                    product = OutsideProduct()
                    product.suppervisionOffice = supervisionOffice
                    product.code = row[0]
                    product.name = row[1]

                    if OutsideCategory.objects.filter(name=row[2],suppervisionOffice=supervisionOffice).count()==0:
                        category = OutsideCategory.objects.create(name=row[2],suppervisionOffice=supervisionOffice)
                    else:
                        category = OutsideCategory.objects.filter(name=row[2],suppervisionOffice=supervisionOffice).first()

                    product.outside_category = category
                    product.unit = row[3]
                    product.price = int(row[4])
                    product.info = row[5]
                    product.save()
        return redirect(f'/backboard/outside_products?supervisionOfficeId={supervisionOfficeId}')

    
    supervisionOffices = SupervisionOffice.objects.all()
    products = OutsideProduct.objects.all().order_by('-id')
    
    # print(supervisionOffices)
    products = products.filter(suppervisionOffice=supervisionOffice)

    
    paginator = Paginator(products, 50)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    # page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/outside_products.html',{'supervisionOffices':supervisionOffices, 'supervisionOfficeId':supervisionOfficeId, 'products':page_obj})

def add_new_outside_product(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    categories = OutsideCategory.objects.filter(suppervisionOffice=supervisionOffice)
 
    if request.method == 'POST':
            supervisionOfficeId = request.POST.get('supervisionOfficeId')
            supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

            product = OutsideProduct()
            product.suppervisionOffice = supervisionOffice
            product.code = request.POST.get('productCode')
            product.name = request.POST.get('productName') 
            category_Id = request.POST.get('productCategory')
            product.outside_category = OutsideCategory.objects.get(id=category_Id)
            product.info = request.POST.get('productInfo')
            product.price = request.POST.get('productPrice')
            if request.POST.get('productUnit') != None:
                product.unit =request.POST.get('productUnit')
            if request.POST.get('productStock') != None:
                product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
        
            return redirect_params('outside_products',{'supervisionOfficeId':product.suppervisionOffice.id})
    
    return render(request, 'backboard/add_new_outside_product.html',{'categories':categories, 'supervisionOfficeId':supervisionOfficeId})
         
def edit_outside_product(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    productId = request.GET.get("productId")
    theProduct = OutsideProduct.objects.get(id=productId)

    supervisionOffice = theProduct.suppervisionOffice
    categories = OutsideCategory.objects.filter(suppervisionOffice=supervisionOffice)
    
    if request.method == 'POST':

        # not related to image
        product = OutsideProduct.objects.get(id=productId)
        product.code = request.POST.get('productCode')
        product.name = request.POST.get('productName')
        category_Id = request.POST.get('productCategory')
        product.outside_category = OutsideCategory.objects.get(id=category_Id)
        product.info = request.POST.get('productInfo')
        product.price = request.POST.get('productPrice')
        product.unit =request.POST.get('productUnit')
        product.stocks = request.POST.get('productStock')
        product.isPublish = request.POST.get('productIspublish')
        product.save()
                    
        # return redirect_params('edit_product',{'productId':productId})

        return redirect_params('outside_products',{'supervisionOfficeId':product.suppervisionOffice.id})
        
    
    return render(request, 'backboard/edit_outside_product.html',{'categories':categories,'productId':productId,'product':theProduct})


def meals(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    

    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    # 匯入
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        file = open(file_path)
        reader = csv.reader(file, delimiter=',')
        for index, row in enumerate(reader):
            if index != 0:
                if Meal.objects.filter(name=row[1],suppervisionOffice=supervisionOffice).count()==0:
                    meal = Meal()
                    meal.suppervisionOffice = supervisionOffice
                    meal.code = row[0]
                    meal.name = row[1]
                    meal.unit = row[2]
                    meal.price = int(row[3])
                    meal.info = row[4]
                    meal.save()
        return redirect(f'/backboard/meals?supervisionOfficeId={supervisionOfficeId}')

    
    supervisionOffices = SupervisionOffice.objects.all()
    meals = Meal.objects.all().order_by('-id')
    
    # print(supervisionOffices)
    meals = meals.filter(suppervisionOffice=supervisionOffice)

    
    paginator = Paginator(meals, 50)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    # page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/meals.html',{'supervisionOffices':supervisionOffices, 'supervisionOfficeId':supervisionOfficeId, 'meals':page_obj})

def add_new_meal(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')
    
    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)
 
    if request.method == 'POST':
            supervisionOfficeId = request.POST.get('supervisionOfficeId')
            supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

            meal = Meal()
            meal.suppervisionOffice = supervisionOffice
            meal.code = request.POST.get('mealCode')
            meal.name = request.POST.get('mealName') 
            meal.info = request.POST.get('mealInfo')
            meal.price = request.POST.get('mealPrice')
            if request.POST.get('mealUnit') != None:
                meal.unit =request.POST.get('mealUnit')
            if request.POST.get('mealStock') != None:
                meal.stocks = request.POST.get('mealStock')
            meal.isPublish = request.POST.get('mealIspublish')
            meal.save()
        
            return redirect_params('meals',{'supervisionOfficeId':meal.suppervisionOffice.id})
    
    return render(request, 'backboard/add_new_meal.html',{'supervisionOfficeId':supervisionOfficeId})
         
def edit_meal(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    mealId = request.GET.get("mealId")
    meal = Meal.objects.get(id=mealId)
    
    if request.method == 'POST':

        # not related to image
        meal = Meal.objects.get(id=mealId)
        meal.code = request.POST.get('mealCode')
        meal.name = request.POST.get('mealName')
        meal.info = request.POST.get('mealInfo')
        meal.price = request.POST.get('mealPrice')
        meal.unit =request.POST.get('mealUnit')
        meal.stocks = request.POST.get('mealStock')
        meal.isPublish = request.POST.get('mealIspublish')
        meal.save()

        return redirect_params('meals',{'supervisionOfficeId':meal.suppervisionOffice.id})
        
    
    return render(request, 'backboard/edit_meal.html',{'mealId':mealId,'meal':meal})


def all_categories(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    if request.GET.get('delete_id') != None:
        try:
            Category.objects.get(id=request.GET.get('delete_id')).delete()
        except:
            print("no such category")

    supervisionOffices = SupervisionOffice.objects.all()
    categories = Category.objects.filter(suppervisionOffice=supervisionOffice)

    return render(request, 'backboard/all_categories.html', {'supervisionOffices':supervisionOffices, 'supervisionOfficeId':supervisionOfficeId, 'categories':categories})

def new_edit_category(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        if request.POST.get('post') == 'save':
            if request.POST.get('name') != None and request.POST.get('name') != '':
                if request.GET.get('category_id') != None:
                    category = Category.objects.get(id=request.GET.get('category_id'))
                    category.name = request.POST.get('name')
                    category.save()
                    return redirect_params('all_categories', {'supervisionOfficeId':category.suppervisionOffice.id})
                else:
                    supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
                    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)
                    Category.objects.create(name=request.POST.get('name'), suppervisionOffice=supervisionOffice)
                    return redirect_params('all_categories', {'supervisionOfficeId':supervisionOfficeId})
        return redirect('all_categories')

    if request.GET.get('category_id') != None:
        category = Category.objects.get(id=request.GET.get('category_id'))
        return render(request, 'backboard/new_edit_category.html', {'category':category})

    return render(request, 'backboard/new_edit_category.html')


def all_outside_categories(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.GET.get('supervisionOfficeId') !=None:
        supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
    else:
        supervisionOfficeId = 1

    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)

    if request.GET.get('delete_id') != None:
        try:
            OutsideCategory.objects.get(id=request.GET.get('delete_id')).delete()
        except:
            print("no such category")

    supervisionOffices = SupervisionOffice.objects.all()
    categories = OutsideCategory.objects.filter(suppervisionOffice=supervisionOffice)

    return render(request, 'backboard/all_outside_categories.html', {'supervisionOffices':supervisionOffices, 'supervisionOfficeId':supervisionOfficeId, 'categories':categories})

def new_edit_outside_category(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('/backboard/')

    if request.method == 'POST':
        if request.POST.get('post') == 'save':
            if request.POST.get('name') != None and request.POST.get('name') != '':
                if request.GET.get('category_id') != None:
                    category = OutsideCategory.objects.get(id=request.GET.get('category_id'))
                    category.name = request.POST.get('name')
                    category.save()
                    return redirect_params('all_outside_categories', {'supervisionOfficeId':category.suppervisionOffice.id})
                else:
                    supervisionOfficeId = int(request.GET.get('supervisionOfficeId'))
                    supervisionOffice = SupervisionOffice.objects.get(id=supervisionOfficeId)
                    OutsideCategory.objects.create(name=request.POST.get('name'), suppervisionOffice=supervisionOffice)
                    return redirect_params('all_outside_categories', {'supervisionOfficeId':supervisionOfficeId})
        return redirect('all_outside_categories')

    if request.GET.get('category_id') != None:
        category = OutsideCategory.objects.get(id=request.GET.get('category_id'))
        return render(request, 'backboard/new_edit_outside_category.html', {'category':category})

    return render(request, 'backboard/new_edit_outside_category.html')



def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response

# def deleteImage(request, id=None):
#     image = get_object_or_404(ProductImage, pk=id)
#     ID = image.product.id
#     your_params = {
#         'productId':ID
#     }
#     image.delete()

    
#     return redirect_params("/backboard/edit_product",your_params)

