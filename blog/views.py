from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

# Create your views here.
def index(request):
    products=Product.objects.filter(trending=1)
    return render(request,'index.html',{"products":products})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method =='POST':
            name=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=name,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('index')
            else:
                messages.error(request,'Invalid User Name or Password')
        return render(request,'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect('/')

def register(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form =CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can Login Now..!')
            return redirect('/login')
    return render(request,'register.html',{"form":form})

def collections(request):
    category=Category.objects.filter(status=0)
    return render(request,'collections.html',{"category":category})

def collectionsview(request,name):
    if(Category.objects.filter(name=name,status=0)):
        products=Product.objects.filter(category__name=name)
        return render(request,'product.html',{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such category found")
        return redirect('collectionsview')
    
def product_details(request,cname,pname):
    if(Category.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'product_details.html',{"products":products})
        else:
            messages.error(request,'No such product found')
            return redirect('collections')
    else:
        messages.error(request,'No Such Category Found')
        return redirect('collections')
    
def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_qty = request.POST.get('product_qty')
            product_id = request.POST.get('pid')

            try:
                product_qty = int(product_qty)
                product_id = int(product_id)
            except (TypeError, ValueError):
                return HttpResponse("Invalid quantity or product ID")

            product_status = Product.objects.filter(id=product_id).first()

            if product_status:
                if Cart.objects.filter(user=request.user, product=product_status).exists():
                    return HttpResponse("Product Already in Cart")
                else:
                    if product_status.quantity >= product_qty:
                        Cart.objects.create(
                            user=request.user,
                            product=product_status,
                            product_qty=product_qty
                        )
                        return HttpResponse(f"{product_status},Product Added to Cart")
                    else:
                        return HttpResponse("Product Stock Not Available")
            else:
                return HttpResponse("No such product found")
        else:
            return HttpResponse("Login to Add Cart")
    else:
        return HttpResponse("Invalid Access")



def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request,'cart.html',{"cart":cart})
    else:
        messages.error(request,"Login to go to cart")
        return redirect('login')
    
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')

def fav_page(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('pid')

            try:
                product_id = int(product_id)
            except (TypeError, ValueError):
                return HttpResponse("Invalid product ID")

            product = Product.objects.filter(id=product_id).first()

            if product:
                fav_item = Favourites.objects.filter(user=request.user, product=product).first()
                if fav_item:
                    fav_item.delete()
                    return HttpResponse(f"{product.name} removed from favourites")
                else:
                    Favourites.objects.create(user=request.user, product=product)
                    return HttpResponse(f"{product.name} added to favourites")
            else:
                return HttpResponse("Product Not Found")
        else:
            return HttpResponse("Login to Add Favourite")
    else:
        return HttpResponse("Invalid Access")



def fav_view_page(request):
    if request.user.is_authenticated:
        fav=Favourites.objects.filter(user=request.user)    
        return render(request,'fav.html',{"cart":fav})
    else:
        
        return redirect('login')
    
def remove_fav(request,fid):
    item=Favourites.objects.get(id=fid)
    item.delete()
    return redirect('fav_view_page')