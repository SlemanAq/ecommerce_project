from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from .models import Product,Customer,Cart, OrderPlaced, Whishlist
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import F, Sum

# Create your views here.

def home(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

def about(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

def contact(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())

class CategoryView(View):
    def get(self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())
    
class ProductDetails(View):
    def get(self,request,pk):

        product = Product.objects.get(pk=pk) #beacuse we only need one product
        wishlist = Whishlist.objects.filter( user = request.user.id, product=product).first()

        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        return render(request,"app/productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.warning(request, "Error! This email is already in use. Please use a different email.")
                return render(request, 'app/customerregistration.html', {'form': form})
            form.save()
            messages.success(request, "Congratulation! User registered successfully")
            return redirect("login")
        else:
            messages.warning(request, "Error! Please check your input data")
        return render(request, 'app/customerregistration.html', {'form': form})
    
@method_decorator(login_required,name='dispatch')   
class profileView(View):
    def get(self,request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Profile save successfully!")
        else:
            messages.warning(request,"Please correct the errors.")
        return render(request, 'app/profile.html',locals())
@login_required    
def address(request):
    address = Customer.objects.filter(user=request.user) 
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals())
@method_decorator(login_required,name='dispatch') 
class updateAdress(View):
    def get(self,request,pk):
        adr = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=adr)
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.user = request.user
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Profile Updated successfully!")
            
        else:
            messages.warning(request,"Please correct the errors.")
        return redirect('address')
    
@method_decorator(login_required, name='dispatch')
class deleteAddress(View):
    def post(self, request, pk):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Whishlist.objects.filter(user=request.user))
        address = get_object_or_404(Customer, pk=pk, user=request.user)
        if request.method == 'POST':
            address.delete()
        return redirect('address')

@login_required    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id = product_id)
    Cart(user=user,product=product).save() #to save product to cart
    return redirect("/cart")
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discount_price
        amount += value
    
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))  
        wishitem = len(Whishlist.objects.filter(user=request.user))
    
    shipping_fee = 10
    totalamount = amount + shipping_fee if amount > 0 else 0
    
    return render(request, 'app/addcart.html', locals())

@method_decorator(login_required,name='dispatch') 
class checkout(View):
    def get(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value= p.quantity * p.product.discount_price
            famount = famount + value
            totalamount = famount + 10

        return render(request,'app/checkout.html',locals())
    def post(self,request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        # customer=Customer.objects.filter(user=user)
        
        for cart_item in cart_items:
            customer = Customer.objects.filter(user=user).first()
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product = cart_item.product,
                quantity = cart_item.quantity,

            )
            cart_item.delete()
        return redirect('orders')
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(product = prod_id,user=request.user).first()# apply multiple conditions
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 10 
        data ={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(product = prod_id,user=request.user).first()# apply multiple conditions
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discount_price
            amount = amount + value
        totalamount = amount + 10 
        data ={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
@login_required    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        c = Cart.objects.filter(product=prod_id, user=request.user).first()
        quantity = 0

        if c:
            quantity = c.quantity  # Store the quantity before deleting
            c.delete()

        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = cart.aggregate(totalamount=Sum(F('quantity') * F('product__discount_price')))['totalamount']
        totalamount = amount + 10 if amount else 0  # Calculate total amount considering shipping fees

        data = {
            'quantity': quantity,
            'amount': amount or 0,  # Set amount to 0 if it's None or 0
            'totalamount': totalamount
        }

        return JsonResponse(data)

    return JsonResponse({'error': 'Invalid request method.'})
    

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))

    order_placed = OrderPlaced.objects.filter(user=request.user)

    # Calculate total cost including shipping fees for each order
    for order in order_placed:
        # Assuming shipping_fee is a fixed value for all orders
        shipping_fee = 10  # You can modify this based on your logic

        # Calculate total cost with shipping fees
        order.total_cost_with_shipping = order.total_cost + shipping_fee

    return render(request, 'app/orders.html', {'order_placed': order_placed, 'totalitem': totalitem, 'wishitem': wishitem})
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Whishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist added successfully'
        }
        return JsonResponse(data)
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Whishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist removed successfully'
        }
        return JsonResponse(data)

    
def search(request):
    query = request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    product = Product.objects.filter(title__icontains=query)
    return render(request,"app/search.html",locals())
@login_required
def show_wishlist(request):
    user = request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Whishlist.objects.filter(user=request.user))
    product = Whishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())
