from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'backboard/orders.html')

def products(request):
    return render(request, 'backboard/products.html')

