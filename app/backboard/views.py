from calendar import month
from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from modelCore.models import User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,ProductOrderShip,PayInfo , ShoppingCart ,OrderState,image_upload_handler
from modelCore.forms import *
import urllib 
from django.db.models import Sum
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    orders = Order.objects.filter(state=1)
    ships = ProductOrderShip.objects.all()
    products =Product.objects.all()
    undealtorders = Order.objects.filter(state=1)
    UndealtOrdersNum = undealtorders.count()
    dealtOrdersShips = Order.objects.filter(state=2)
    last7Days = (datetime.today() - timedelta(days=7)).date()
    last6Days = (datetime.today() - timedelta(days=6)).date()
    last5Days = (datetime.today() - timedelta(days=5)).date()
    last4Days = (datetime.today() - timedelta(days=4)).date()
    last3Days = (datetime.today() - timedelta(days=3)).date()
    last2Days = (datetime.today() - timedelta(days=2)).date()
    last1Days = (datetime.today() - timedelta(days=1)).date()
    WeekOrders = dealtOrdersShips.filter(createDate__date__gte=last7Days)
    last7DaysOrders = dealtOrdersShips.filter(createDate__date=last7Days)
    last6DaysOrders = dealtOrdersShips.filter(createDate__date=last6Days)
    last5DaysOrders = dealtOrdersShips.filter(createDate__date=last5Days)
    last4DaysOrders = dealtOrdersShips.filter(createDate__date=last4Days)
    last3DaysOrders = dealtOrdersShips.filter(createDate__date=last3Days)
    last2DaysOrders = dealtOrdersShips.filter(createDate__date=last2Days)
    last1DaysOrders = dealtOrdersShips.filter(createDate__date=last1Days)
    sum7=0
    sum6=0
    sum5=0
    sum4=0
    sum3=0
    sum2=0
    sum1=0
    sum7Money=0 
    sum6Money=0
    sum5Money=0
    sum4Money=0
    sum3Money=0
    sum2Money=0
    sum1Money=0
    for last7DaysOrder in last7DaysOrders:
        ships7 = ships.filter(order=last7DaysOrder)
        for ship in ships7:
            sum7 += ship.amount
            sum7Money += ship.product.price * ship.amount
    for last6DaysOrder in last6DaysOrders:
        ships6 = ships.filter(order=last6DaysOrder)
        for ship in ships6:
            sum6 += ship.amount
            sum6Money += ship.product.price * ship.amount
    for last5DaysOrder in last5DaysOrders:
        ships5 = ships.filter(order=last5DaysOrder)
        for ship in ships5:
            sum5 += ship.amount
            sum5Money += ship.product.price * ship.amount
    for last4DaysOrder in last4DaysOrders:
        ships4 = ships.filter(order=last4DaysOrder)
        for ship in ships4:
            sum4 += ship.amount
            sum4Money += ship.product.price * ship.amount
    for last3DaysOrder in last3DaysOrders:
        ships3 = ships.filter(order=last3DaysOrder)
        for ship in ships3:
            sum3 += ship.amount
            sum3Money += ship.product.price * ship.amount
    for last2DaysOrder in last2DaysOrders:
        ships2 = ships.filter(order=last2DaysOrder)
        for ship in ships2:
            sum2 += ship.amount
            sum2Money += ship.product.price * ship.amount
    for last1DaysOrder in last1DaysOrders:
        ships1 = ships.filter(order=last1DaysOrder)
        for ship in ships1:
            sum1 += ship.amount
            sum1Money += ship.product.price * ship.amount
    for product in products:
        sum = 0
        for WeekOrder in WeekOrders:
            OrderShips=ships.filter(order=WeekOrder,product=product)       
            for OrderShip in OrderShips:
                sum += OrderShip.amount                 
        product.week_sum_nums = sum      
        product.save()   
    sumtotal= sum1 + sum2 + sum3 + sum4 + sum5 + sum6 + sum7
    sumTotalMoney = sum1Money +sum2Money + sum3Money +sum4Money + sum5Money+ sum6Money + sum7Money
    forlooplist = []
    last10Orders = orders.order_by('-createDate')[:10]
    for order in last10Orders:
        sum = 0
        TotalMoney = ships.filter(order=order).aggregate(Sum('money'))
        if TotalMoney['money__sum'] != None:
            sum += TotalMoney['money__sum']
            forlooplist.append({'sum':sum,'order':order})
    
    productRank = Product.objects.order_by("-week_sum_nums")[:3]
    
    return render(request, 'backboard/index.html',{'sumTotalMoney':sumTotalMoney, 'sumtotal':sumtotal, 'forlooplist':forlooplist, 'sum7Money':sum7Money,'sum6Money':sum6Money,'sum5Money':sum5Money,'sum4Money':sum4Money,'sum3Money':sum3Money,'sum2Money':sum2Money,'sum1Money':sum1Money, 'sum1':sum1,'sum2':sum2,'sum3':sum3,'sum4':sum4,'sum5':sum5,'sum6':sum6,'sum7':sum7, 'last6Days':last6Days,'last5Days':last5Days,'last4Days':last4Days ,'last3Days':last3Days,'last2Days':last2Days,'last1Days':last1Days, 'last7Days':last7Days, 'orders':orders,'UndealtOrdersNum':UndealtOrdersNum,'productRank':productRank})

def base(request):
    return render(request, 'backboard/base.html')


def bills(request):
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
    customers = User.objects.all()
    customers.order_by('-id')

    paginator = Paginator(customers, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    
    for customer in customers:
        
        customer_id=customer.id
    return render(request, 'backboard/customers.html',{'customers':page_obj,'customer_id':customer_id})

def customer_detail(request):
    customers = User.objects.all()
    orders = Order.objects.all()
    customer_id = request.GET.get('customer_id','')
    customers = customers.filter(id=customer_id)
    ships = ProductOrderShip.objects.all()
    forlooplist=[] 
    for order in orders:
        sum = 0
        if order.user == customers.get(id=customer_id):
                
                TotalMoney = ships.filter(order=order).aggregate(Sum('money'))
                if TotalMoney['money__sum'] != None:
                    sum += TotalMoney['money__sum']
                    forlooplist.append({'user':order.user ,'sum':sum,'order':order})
    return render(request, 'backboard/customer_detail.html',{'forlooplist':forlooplist, 'orders':orders,'customers':customers})

def orders(request):
    
    
    orders = Order.objects.all()
    users = User.objects.all()
    orderstates = OrderState.objects.all()
    ships = ProductOrderShip.objects.all()
    q = request.GET.get('order_state')
    if q != None:
        theOrderstate = orderstates.get(id=request.GET.get('order_state'))      
        theOrders = orders.filter(state=theOrderstate)  
    else:
        theOrders = orders
    forlooplist=[] 
    for theOrder in theOrders:
        sum = 0
        TotalMoney = ships.filter(order=theOrder).aggregate(Sum('money'))
        if TotalMoney['money__sum'] != None:
                sum += TotalMoney['money__sum']
                forlooplist.append({'user':theOrder.user ,'sum':sum,'order':theOrder})
    for order in orders:
        IdOder=order.id

    
    
    paginator = Paginator(forlooplist, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/orders.html',{'q':q, 'forlooplist':page_obj, 'orders':orders,'users':users,'IdOder':IdOder,'orderstates':orderstates})
    

def order_detail(request):
    orders = Order.objects.all()
    users = User.objects.all()
    payinfos=PayInfo.objects.all()
    orderstates = OrderState.objects.all()
    products=Product.objects.all()
    ships = ProductOrderShip.objects.all()
    
    order_id=request.GET.get('IdOrder')
    order = orders.get(id=order_id)
    sum = 0
    forlooplist=[]
   
    for ship in ships:
        if ship.order == order:
            TotalMoney = ship.money
            if TotalMoney != None:
                sum += TotalMoney
                forlooplist.append({'money':TotalMoney,'order':order,'ship':ship})
                
   
    if order_id != None:        
        
        theOrder = Order.objects.get(id=order_id)
    else:
        
        theOrder = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        
        State_Id = request.POST.get('OrderState')
        
        theOrder.state = OrderState.objects.get(id=State_Id)
        theOrder.save()

        return redirect('/backboard/orders')

    return render(request, 'backboard/order_detail.html',{'order':order ,'sum':sum, 'forlooplist':forlooplist, 'orders':orders,'users':users,'payinfos':payinfos,'products':products,'orderstates':orderstates,'ships':ships,'sum':sum})


def products(request):
    products = Product.objects.all()
    ships = ProductSupervisionOfficeShip.objects.all()
    productimages = ProductImage.objects.all()
    
    products.order_by('-id')
    
    paginator = Paginator(products, 10)
    if request.GET.get('page') != None:
        page_number = request.GET.get('page') 
    else:
        page_number = 1
    page_obj = paginator.get_page(page_number)

    page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number)

    return render(request, 'backboard/products.html',{'products':page_obj,'ships':ships,'productimages':productimages})


def offices_order(request):
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


def add_new_product(request):

    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    form = ProductImageForm()
    ships = ProductSupervisionOfficeShip.objects.all()
    productimages = ProductImage.objects.order_by('-id')
    list=[]
 
    if request.method == 'POST':

            form = ProductImageForm(request.POST, request.FILES)
            form.save()
            img_obj = form.instance
            product = Product()
            productName = request.POST.get('productName') 
            product.name = productName
            category_Id = request.POST.get('productCategory')
            product.category = Category.objects.get(id=category_Id)
            product.sublabel =request.POST.get('productSublabel')
            product.info = request.POST.get('productInfo')
            product.content = request.POST.get('productContent')
            product.price = request.POST.get('productPrice')
            product.unit =request.POST.get('productUnit')
            product.stocks = request.POST.get('productStock')
            product.isPublish = request.POST.get('productIspublish')
            product.save()
            office_dict={}
            office_list=[]

            for i in range(1,supervisionoffices.count()+1):  
                strcombine = ''.join(['ship_officeId', str(i)])
                office_dict['officeId'+str(i)]=request.POST.get(strcombine)
                ship = ProductSupervisionOfficeShip.objects.filter(product=product,supervisionOffice=i)
                office = SupervisionOffice.objects.get(id=i)
                if office_dict['officeId'+str(i)] ==  ''.join(['check_office_', str(i)]):
                    

                    if ship.exists() :
                        pass
                    else:
                        productsupervisionOfficeship = ProductSupervisionOfficeShip()
                        productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=i)
                        productsupervisionOfficeship.product = product
                        productsupervisionOfficeship.save()
                        
                else:
                    
                    if ship.exists() :
                        ship.delete()
                    else:
                        pass
                office_list.append({'office':office})
            
            
            img_obj.product = product
            img_obj.save()
        
            return redirect('/backboard/products')
    else:
        form = ProductImageForm()
        form.initial['product'] = Product.objects.latest('id')
    
    
    return render(request, 'backboard/add_new_product.html',{ 'ships':ships, 'productimages':productimages, 'list':list, 'supervisionoffices':supervisionoffices,'categories':categories, 'form':form})
         

def edit_product(request):
    
    products = Product.objects.all()
    form = ProductImageForm()
    productId = request.GET.get("productId")
    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    # ProductQueryset = Product.objects.filter(id=productId)
    theproduct = Product.objects.get(id=productId)
    productships = ProductSupervisionOfficeShip.objects.filter(product=theproduct)
    
    productimages = ProductImage.objects.filter(product=theproduct).order_by('-id')
    
    if request.method == 'POST':
    
        submitValue = request.POST.get('submit')

        # related to image
        if submitValue == "upload_image":
            form = ProductImageForm(request.POST, request.FILES)
            form.save()

            img_obj = form.instance
            
            render(request, 'backboard/edit_product.html',{'supervisionoffices':supervisionoffices,'categories':categories,'productships':productships,'products':products,'productId':productId,'product':theproduct,'form':form, 'img_obj': img_obj})

        # not related to image
        product = Product.objects.get(id=productId)
        category_Id = request.POST.get('productCategory')
        product.name = request.POST.get('productName')
        product.category = Category.objects.get(id=category_Id)
        product.sublabel =request.POST.get('productSublabel')
        product.info = request.POST.get('productInfo')
        product.content = request.POST.get('productContent')
        product.price = request.POST.get('productPrice')
        product.unit =request.POST.get('productUnit')
        product.stocks = request.POST.get('productStock')
        product.isPublish = request.POST.get('productIspublish')
        product.save()
        office_dict={}
        for i in range(1,supervisionoffices.count()+1):  
            strcombine = ''.join(['ship_officeId', str(i)])
            office_dict['officeId'+str(i)]=request.POST.get(strcombine)
            ship = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=i)
                
            if office_dict['officeId'+str(i)] ==  ''.join(['check_office_', str(i)]):
 
                if ship.exists() :
                    
                    pass
                else:
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=i)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()
                    
            else:
                if ship.exists() :
                    ship.delete()
                    
                else:
                    pass
                    
        
            
        return redirect_params('edit_product',{'productId':productId})
            
    else:
        
        form = ProductImageForm()
        form.initial['product'] = theproduct
        
    
    return render(request, 'backboard/edit_product.html',{'supervisionoffices':supervisionoffices,'productimages':productimages,'categories':categories,'productships':productships,'products':products,'productId':productId,'product':theproduct,'form':form})

def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urllib.parse.urlencode(params)
        response['Location'] += '?' + query_string
    return response

def deleteImage(request, id=None):
    image = get_object_or_404(ProductImage, pk=id)
    ID = image.product.id
    your_params = {
        'productId':ID
    }
    image.delete()

    
    return redirect_params("/backboard/edit_product",your_params)

