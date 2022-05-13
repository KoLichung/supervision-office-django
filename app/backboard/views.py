from django.shortcuts import render ,redirect
from django.http import HttpResponse
import requests
from modelCore.models import User , Category, Product , ProductImage , SupervisionOffice , ProductSupervisionOfficeShip ,Order ,PayInfo , ShoppingCart ,OrderState



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
    orderstates = OrderState.objects.all()
    orderstate_id1 = request.GET.get('order_state1')
    orderstate_id2 = request.GET.get('order_state2')
    orderstate_id3 = request.GET.get('order_state3')
    theOrderstate1 = orderstates.filter(id=orderstate_id1)
    theOrderstate2 = orderstates.filter(id=orderstate_id2)
    theOrderstate3 = orderstates.filter(id=orderstate_id3)
    for order in orders:
        order_id=order.id
    # if request.method == 'POST':

    return render(request, 'backboard/orders.html',{'orders':orders,'users':users,'order_id':order_id,'orderstates':orderstates,'theOrderstate1':theOrderstate1,'theOrderstate2':theOrderstate2,'theOrderstate3':theOrderstate3})
    

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
        
        product = Product()
        
        product.name = request.POST.get('productName') 
        
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
        
        
        ship_officeId1 =request.POST.get('ship_officeId1')
        ship_officeId2 =request.POST.get('ship_officeId2')
        ship_officeId3 =request.POST.get('ship_officeId3')
        

        
        
        if ship_officeId1 == "1":
            productsupervisionOfficeship = ProductSupervisionOfficeShip()
            productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId1)
            productsupervisionOfficeship.product = product
            productsupervisionOfficeship.save()

        if ship_officeId2 == "2":
            productsupervisionOfficeship = ProductSupervisionOfficeShip()
            productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId2)
            productsupervisionOfficeship.product = product
            productsupervisionOfficeship.save()

        if ship_officeId3 == "3":
            productsupervisionOfficeship = ProductSupervisionOfficeShip()
            productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=ship_officeId3)
            productsupervisionOfficeship.product = product
            productsupervisionOfficeship.save()

        
        return redirect('/backboard/products')

    return render(request, 'backboard/add_new_product.html',{'supervisionoffices':supervisionoffices,'categories':categories})
        

def edit_product(request):
    
    products = Product.objects.all()
    
    productId = request.GET.get("productId")
    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    ProductQueryset = Product.objects.filter(id=productId)
    theproduct = Product.objects.get(id=productId)
    productships = ProductSupervisionOfficeShip.objects.filter(product=theproduct)
    ship1 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=1)
    ship2 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=2)
    ship3 = ProductSupervisionOfficeShip.objects.filter(product=theproduct,supervisionOffice=3)
    
    for ship in productships:
        print(ship.supervisionOffice.id)
    
   

    if request.method == 'POST':
        
        
        
        if theproduct.name == request.POST.get('productName'):
            product = Product.objects.get(id=productId)
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
            
            
            officeId1=request.POST.get('ship_officeId1')
            officeId2=request.POST.get('ship_officeId2')
            officeId3=request.POST.get('ship_officeId3')
            
            
            
            
            
            
            if officeId1 == "1" :
                print("officeId1:",officeId1)
                if ship1.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship1')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=1)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship1.exists() :
                    print('delete ship1')
                    ship1.delete()
                else:
                    print('pass2')
                    pass



            if officeId2 == "2" :
                print("officeId2:",officeId2)
                if ship2.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship2')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=2)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship2.exists() :
                    print('delete ship2')
                    ship2.delete()
                else:
                    print('pass2')
                    pass

            if officeId3 == "3" :
                print("officeId3:",officeId3)
                if ship3.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship3')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=3)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship3.exists() :
                    print('delete ship3')
                    ship3.delete()
                else:
                    print('pass2')
                    pass

            return redirect('/backboard/products')


        elif Product.objects.filter(name=request.POST.get('productName')).exists() == False :
            
            product = Product.objects.get(id=productId)
            product.name = request.POST.get('productName')
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
            
            
            officeId1=request.POST.get('ship_officeId1')
            officeId2=request.POST.get('ship_officeId2')
            officeId3=request.POST.get('ship_officeId3')
            
            
            
            
            
            
            if officeId1 == "1" :
                print("officeId1:",officeId1)
                if ship1.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship1')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=1)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship1.exists() :
                    print('delete ship1')
                    ship1.delete()
                else:
                    print('pass2')
                    pass



            if officeId2 == "2" :
                print("officeId2:",officeId2)
                if ship2.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship2')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=2)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship2.exists() :
                    print('delete ship2')
                    ship2.delete()
                else:
                    print('pass2')
                    pass

            if officeId3 == "3" :
                print("officeId3:",officeId3)
                if ship3.exists() :
                    print('pass1')
                    pass
                else:
                    print('add ship3')
                    productsupervisionOfficeship = ProductSupervisionOfficeShip()
                    productsupervisionOfficeship.supervisionOffice = SupervisionOffice.objects.get(id=3)
                    productsupervisionOfficeship.product = product
                    productsupervisionOfficeship.save()

            else:
                if ship3.exists() :
                    print('delete ship3')
                    ship3.delete()
                else:
                    print('pass2')
                    pass
            
            return redirect('/backboard/products')


        else:
            pass
    
    return render(request, 'backboard/edit_product.html',{'supervisionoffices':supervisionoffices,'categories':categories,'productships':productships,'products':products,'productId':productId,'ProductQueryset':ProductQueryset})
        