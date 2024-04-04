from django.shortcuts import render, HttpResponse, redirect
from .import views
from django.http import JsonResponse
from .forms import Enquiryform, Supportform, cartform
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import razorpay

import random                                                                                                                                                                       


def home(request):
    slider= Slider.objects.all()

    categorydata= Category.objects.all()
    prod={}
    for x in categorydata:
        prod[x]= Product.objects.filter(category=x)[:4]

    context= {'cdata': categorydata , 'slider': slider, 'products':prod}

   

    return render(request, 'skapp/index.html', context)


def search(request):
    q= request.POST.get('search')
    data= Product.objects.filter(name__icontains=q)
    context={'data': data}
    return render(request, 'skapp/search.html', context)

    

def cart(request):
        userid= request.user.id
        cartdata= cartModel.objects.filter(userid=userid)

        total=0
        for x in cartdata:
            mrp= str(x.pid.mrp)
            newmrp= float(mrp.replace(",", ""))
            total+= newmrp * x.qty

        if total>=1000: 
            sc=0
        else:
            sc=50  

        gst= 18    

        netamount= total+ total*gst/100+ sc        
        context= {'cart': cartdata, 'total': total, 'net': netamount, 'sc': sc, 'gst':gst }
        return render(request, 'skapp/cart.html', context)

@login_required
def add_to_cart(request):
    userid= request.user
    pid= request.POST.get('pid')
    productData= get_object_or_404(Product, id=pid)

    cart, created = cartModel.objects.get_or_create(userid=userid, pid=productData)
    if not created:
        cart.qty+=1
        cart.save()
    
    return redirect('cart')

def delete_cart(request, id):
    cart= cartModel.objects.get(id=id)
    cart.delete()
    return redirect('cart')

def updatecart(request):
    newqty= request.POST.get('qtychange')
    cartid= request.POST.get('cartid')
    cartData= cartModel.objects.get(id=cartid)
    cartData.qty= newqty
    cartData.save()
    return HttpResponse('Cart Updated')


def about(request):
    return render(request, 'skapp/about.html')

def contactPage(request):
    if request.method=="POST":
        form= Enquiryform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'skapp/contact.html', {'msg': "Thanks for contacting with Us !!!"})


    return render(request, 'skapp/contact.html')

def productPage(request):
    
    data= Product.objects.all()
    context= {'data': data}
    return render(request, 'skapp/products.html', context)

def categoryProducts(request, id):
    data= Product.objects.filter(category=id)
    context= {'data': data} 
    return render(request, 'skapp/category-products.html', context) 


def support(request):
   if request.method=="POST":
        form= Supportform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'skapp/support.html', {'msg': "Thanks for contacting with Us !!!"})
   return render(request, 'skapp/support.html')

def details(request, id):
    data= Product.objects.get(id=id)
    context= {'data': data}
    return render(request, 'skapp/details.html', context)

def signup(request):
    msg={}

    if request.method=="POST":
        username= request.POST.get('username')
        email= request.POST.get('email')
        password1= request.POST.get('password1')
        password2= request.POST.get('password2')
        
        if password1==password2:
            user= User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            msg= {'msg': "User Account Created Successfully"}
        else:
            msg= {'msg': "Passwords Must Be Same"}
           
    return render(request,  'skapp/signup.html', msg)

def userlogin(request):
    msg={}
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password1')
        user= authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('my-account')

        else:
            msg={'msg': "Invalid Username Or Password"}


    return render(request, 'skapp/login.html', msg)

@login_required
def myaccount(request):
        orderData= OrderItems.objects.filter(userid= request.user)
        

        if(request.method=="POST"):
            tid= request.POST.get('trackingid')
            tracking= OrderItems.objects.get(orderid=tid)
            trackingData= orderTracking.objects.filter(trackingid=tracking.id)
            context={'orders': orderData, 'trackingData': trackingData}
        
        else:
            context={'orders': orderData}

        return render(request, 'skapp/my-account.html', context)
    

def userlogout(request):
    logout(request)
    return redirect('login')

def checkout(request):

    userid= request.user.id

    selectedItems= request.POST.get('pids').split(',')
    
    cartdata= cartModel.objects.filter(userid=userid, pid__in=selectedItems)

    total=0
    for x in cartdata:
        mrp= str(x.pid.mrp)
        newmrp= float(mrp.replace(",", ""))
        total+= newmrp * x.qty

    if total>=1000: 
        sc=0
    else:
        sc=50  
    gst= 18 
       
    netamount= total+ total*gst/100+ sc        
    countries = country.objects.all()
    context= {'cart': cartdata, 'total': total, 'net': netamount, 'sc': sc, 'gst':gst, 'countries': countries }
    return render(request, 'skapp/checkout.html', context)

def getStates(request):
    cid= request.GET.get('cid')
    states= state.objects.filter(cid=cid).values('id', 'name')
    return JsonResponse(list(states), safe=False)

def getCity(request):
    sid= request.GET.get('sid')
    citydata= city.objects.filter(sid=sid).values('id', 'name')
    return JsonResponse(list(citydata), safe=False)

def sendOrder(request):
    order= Order()
    if request.method=="POST":
        order.userid= request.user
        order.first_name= request.POST.get('fname') 
        order.last_name= request.POST.get('lname')
        order.email= request.POST.get('email')
        order.contact= request.POST.get('contact')
        order.address= request.POST.get('addline1')+','+request.POST.get('addline2')
        order.country= request.POST.get('country')
        order.state= request.POST.get('state')
        order.city=request.POST.get('city')
        order.pincode=request.POST.get('pincode')
        order.message=request.POST.get('message')
        order.orderamt=request.POST.get('totalamt')
        

        trackingno= "SKORD"+str(random.randint(111111, 999999))
        order.trackingno=trackingno
        order.payment_mode= request.POST.get('paymode')
        order.save()

        
        cartitems= cartModel.objects.filter(userid=request.user)

        for x in cartitems:
            neworders= OrderItems()
            neworders.userid= request.user
            neworders.productid= x.pid
            productData= Product.objects.filter(title=x.pid).first()
            productData.stock= productData.stock-x.qty
            productData.save()    

            neworders.order_qty=x.qty
            neworders.orderid=trackingno
            neworders.save()

        cartdata= cartModel.objects.filter(userid=request.user)
        cartdata.delete()

        currentOrder= OrderItems.objects.filter(orderid=trackingno)

        if order.payment_mode=="offline":
            return render(request, 'skapp/order-confirm.html', {'trn': trackingno, 'currentorders': currentOrder})
        else:
            return render(request, 'skapp/payment.html', {'amount': float(request.POST.get('totalamt'))*100})

def OrderHistory(request):   
   pass


@csrf_exempt
def complete_payment(request):
 if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        return render(request,"skapp/payment-success.html", {'amount': amount*100 })


# def Profile(request):
#     return render(request, 'skapp/profile.html')


        






