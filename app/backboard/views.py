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
    q = request.GET.get('order_state')
    if q != None:
        theOrderstates = orderstates.filter(id=request.GET.get('order_state'))
        
    else:
        theOrderstates = orderstates
        
    
    
    for order in orders:
        IdOder=order.id
    
        


        

    return render(request, 'backboard/orders.html',{'orders':orders,'users':users,'IdOder':IdOder,'orderstates':orderstates,'theOrderstates':theOrderstates})
    

def order_detail(request):
    orders = Order.objects.all()
    users = User.objects.all()
    payinfos=PayInfo.objects.all()
    orderstates = OrderState.objects.all()
    products=Product.objects.all()
    
    
    order_id=request.GET.get('IdOrder')
    orders = orders.filter(id=order_id)
    if order_id != None:        
        
        theOrder = Order.objects.get(id=order_id)
    else:
        print('order_id:',order_id)
        theOrder = Order.objects.get(id=order_id)
    
    if request.method == 'POST':
        
        State_Id = request.POST.get('OrderState')
        
        theOrder.state = OrderState.objects.get(id=State_Id)
        theOrder.save()

        return redirect('/backboard/orders')

    return render(request, 'backboard/order_detail.html',{'orders':orders,'users':users,'payinfos':payinfos,'products':products,'orderstates':orderstates})


def products(request):
    products = Product.objects.all()
    ships = ProductSupervisionOfficeShip.objects.all()
    return render(request, 'backboard/products.html',{'products':products,'ships':ships})

def add_new_product(request):

    supervisionoffices = SupervisionOffice.objects.all()
    categories = Category.objects.all()
    

    if request.method == 'POST':
        if Product.objects.filter(name=request.POST.get('productName')).exists() == False :
            product = Product()
            product_img = ProductImage()
            
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
            
            product_img.product = Product.objects.get(name=request.POST.get('productName'))
            product_img.image = request.POST.get('upload_img')
            product_img.save()
            
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

            else:
                pass
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
        