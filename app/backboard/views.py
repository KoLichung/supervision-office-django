from django.shortcuts import render ,redirect
from django.http import HttpResponse
import requests
from modelCore.models import User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart



# Create your views here.

def index(request):
    return render(request, 'backboard/index.html')

def base(request):
    return render(request, 'backboard/base.html')

def add_new_product(request):
    return render(request, 'backboard/add_new_product.html')

def bills(request):
    return render(request, 'backboard/bills.html')

def customers(request):
    customers = User.objects.all()
    
    for customer in customers:
        
        customer_id=customer.id
    return render(request, 'backboard/customers.html',{'customers':customers,'customer_id':customer_id})

def customer_detail(request):
    customers = User.objects.all()
    orders = Order.objects.all()
    customer_id = request.GET.get('customer_id','')
    customers = customers.filter(id=customer_id)
    
    for order in orders:
        if order.user == customers.get(id=customer_id):
                order_id = order.id
    return render(request, 'backboard/customer_detail.html',{'orders':orders,'customers':customers,'order_id':order_id})

def orders(request):
    
    
    orders = Order.objects.all()
    users = User.objects.all()
    for order in orders:
        order_id=order.id
    return render(request, 'backboard/orders.html',{'orders':orders,'users':users,'order_id':order_id})
    

def order_detail(request):
    orders = Order.objects.all()
    users = User.objects.all()
    payinfos=PayInfo.objects.all()
    products=Product.objects.all()
    
    if request.GET.get('order_id') != None:
            order_id=request.GET.get('order_id', '')        
    else:
            order_id = 1 
    orders = orders.filter(id=order_id)
    return render(request, 'backboard/order_detail.html',{'orders':orders,'users':users,'payinfos':payinfos,'products':products})


def products(request):
    products = Product.objects.all()
    ships = ProductSupervisionOfficeShip.objects.all()
    return render(request, 'backboard/products.html',{'products':products,'ships':ships})

def add_new_product(request):

    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        a
        product = Product()
        ship = ProductSupervisionOfficeShip()
        product.name = request.POST.get('productName') 
        product.category = request.POST.get('productCategory')
        product.sublabel =request.POST.get('productSublabel')
        product.info = request.POST.get('productInfo')
        product.content = request.POST.get('productContent')
        product.price = request.POST.get('productPrice')
        product.unit =request.POST.get('productUnit')
        product.stocks = request.POST.get('productStock')
        product.isPublish = request.POST.get('productIspublish')
        product.save()

        ship_office =request.POST.get('ship_office')
        ship.supervisionOffice = SupervisionOffice.objects.get(name=ship_office)
        ship_product =request.POST.get('ship_product')
        ship.product = Product.objects.get(name=ship_product)
        
        ship.save()
        return redirect('/backboard/products')

    return render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories})
        




