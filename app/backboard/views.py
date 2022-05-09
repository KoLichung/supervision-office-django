from django.shortcuts import render
from django.http import HttpResponse
import requests
from modelCore.models import User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart



# Create your views here.

def index(request):
    return render(request, 'backboard/index.html')

def add_new_product(request):
    return render(request, 'backboard/add_new_product.html')

def bills(request):
    return render(request, 'backboard/bills.html')

def customers(request):
    return render(request, 'backboard/customers.html')

def order_detail(request):
    return render(request, 'backboard/order_detail.html')

def orders(request):
    
    orders = Order.objects.order_by('id')
    users = User.objects.all()
    return render(request, 'backboard/orders.html',{'orders':orders,'users':users})

def order_detail(request):
    orders = Order.objects.order_by('id')
    users = User.objects.all()
    payinfos=PayInfo.objects.all()
    products=Product.objects.all()
    return render(request, 'backboard/order_detail.html',{'orders':orders,'users':users,'payinfos':payinfos,'products':products})


def products(request):
    return render(request, 'backboard/products.html')

