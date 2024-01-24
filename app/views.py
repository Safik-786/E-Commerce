from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
# from .forms.post_forms import CustomerRegistrationForm
from .form import CustomerRegistrationForm, CustomerProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# classbased view rendering and filtering

class ProductView(View):
    def get(self,request):
        totalitem= 0;
        topwears= Product.objects.filter(category='TW')
        bottomwears= Product.objects.filter(category='BW')
        mobiles= Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user= request.user))
        return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'totalitem':totalitem})
# def home(request):
#     bottomwears= Product.objects.filter(category='BW')
#     print(bottomwears)
#     return render(request, 'app/home.html')
#     return render(request, 'app/home.html')



class ProductDetailView(View):
    def get(self , request , pk ):
        totalitem= 0
        product= Product.objects.get(pk=pk)
        item_in_cart= False
        if request.user.is_authenticated:            
            totalitem= len(Cart.objects.filter(user= request.user))
            item_in_cart= Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product': product, 'item_in_cart': item_in_cart,'totalitem':totalitem})
# def product_detail(request):
#  return render(request, 'app/productdetail.html')

@login_required
def add_to_cart(request):
    user= request.user
    product_id= request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user, product=product ).save()
    return redirect('/cart')

@login_required
def showCart(request):
    totalitem= 0;
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user= request.user))
        user= request.user
        cart= Cart.objects.filter(user=user)
        amount= 0.0;
        shipping_amount= 50.0
        total_amount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user == user ]  # query set to  list converter
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount += tempamount
                total_amount= amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount': total_amount, "amount":amount,'totalitem':totalitem})
        else:
            return render(request, 'app/emptycart.html')


def plus_cart(request):
    if request.method== 'GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity+=1
        c.save()
        amount= 0.0;
        user= request.user
        shipping_amount= 50.0
        total_amount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user == user ]  # query set to  list converter
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount += tempamount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)
        
def minus_cart(request):
    if request.method== 'GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity-=1
        c.save()
        amount= 0.0;
        user= request.user
        shipping_amount= 50.0
        total_amount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user == user ]  # query set to  list converter
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount += tempamount
            data={
                'quantity':c.quantity,
                'amount':amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method== 'GET':
        prod_id= request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.delete()
        amount= 0.0;
        user= request.user
        shipping_amount= 50.0
        total_amount= 0.0
        cart_product= [p for p in Cart.objects.all() if p.user == user ]  # query set to  list converter
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount += tempamount
            data={
                'amount':amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)
        
    
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
    add= Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'addr':add, 'active':'btn-danger'})

@login_required
def orders(request):
    op= OrderPlaced.objects.filter(user=request.user)
    totalitem=0
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user= request.user))
    return render(request, 'app/orders.html', {'order_placed':op,'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobiles= Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung' or data == 'apple' or data == '1plus' :
        mobiles= Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below' :
        mobiles= Product.objects.filter(category='M').filter(discount_price__lt=25000)
    elif data == 'above' :
        mobiles= Product.objects.filter(category='M').filter(discount_price__gt=25000)
         
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

def topwear(request, data=None):
    if data == None:
        topwears= Product.objects.filter(category='TW')
    elif data == 'below' :
        topwears= Product.objects.filter(category='TW').filter(discount_price__lt=900)
    elif data == 'above' :
        topwears= Product.objects.filter(category='TW').filter(discount_price__gt=900)
         
    return render(request, 'app/topWear.html', {'topwears':topwears})

# def login(request):
#  return render(request, 'app/login.html')

def CustomeRegistrationView(request):
    if request.method == 'POST':
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulation! Registered Successfully")
            form.save()
    else:
        form= CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':form})

# class CustomeRegistrationView(View):
#     def get(self, request):
#         form= UserCreationForm()
#         return render(request,'app/customerregistration.html',{'form':form} )
#     def post(self, request):
#         form= UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return render(request,'app/customerregistration.html',{'form':form} )
    
@login_required 
def checkout(request):
    user= request.user
    addr= Customer.objects.filter(user=user)
    cart_item= Cart.objects.filter(user=user)
    amount= 0.0
    shipping_amount= 70.0
    totalamount= 0.0
    cart_product= [p for p in Cart.objects.all() if p.user == user ]  
    if cart_product:
        for p in cart_product:
            tempamount= (p.quantity * p.product.discount_price)
            amount += tempamount
        totalamount= amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':addr, "totalamount":totalamount, 'cartitems': cart_item})

@login_required
def payment_done(request):
    user= request.user
    custid= request.GET.get('custid')
    customer= Customer.objects.get(id=custid)
    cart= Cart.objects.filter(user=user)
    for c in cart :
        OrderPlaced(user=user, customer=customer, product= c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('/orders')


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')

@method_decorator(login_required, name='dispatch')
class Profile(View):
    def get(self, request):
        totalitem= 0
        form= CustomerProfileForm()
        add= Customer.objects.filter(user=request.user)
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user= request.user))
        return render(request, 'app/profile.html', {'form':form,  'active':'btn-danger', 'ad':add, 'totalitem':totalitem})
    def post(self, request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            usr= request.user
            name= form.cleaned_data['name']
            locality= form.cleaned_data['locality']
            city= form.cleaned_data['city']
            state= form.cleaned_data['state']
            zipcode= form.cleaned_data['zipcode']
            reg= Customer(user= usr, name=name, locality=locality, city=city , state= state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully ')
        return render(request, 'app/profile.html', {'form':form,  'active':'btn-danger'})


def logout_view(request):
    logout(request)
    return redirect('/accounts/login')