from typing import get_args
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
import json 
from .for_guests import guest_cart
import datetime 
from django.contrib.auth.forms import UserCreationForm
from .forms import create_user_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.db.models import Q

def signup(request):
    form = create_user_form()
    if request.method == 'POST':
        form = create_user_form(request.POST)
        if form.is_valid():
            form.save()
            print(form.save)
            username=request.POST.get('username')
            password= request.POST.get('password')
            email=request.POST.get('email')
            user = form.save()
            #so that user has a customer and no error is returned  
            Customer.objects.create(user=user,name=username,email=email)

            messages.success(request, 'Your account was successfully created! You can log in now')
            return redirect('login')
            

    context={'form': form}
    return render(request, 'web_project/signup.html', context)

def loginpage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(request, username=username, password=password)
       
        if user is not None:
            login(request, user)
            return redirect('store')

    context={}
    return render(request, 'web_project/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('store')


def about(request):
    return render(request, 'web_project/about.html')

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems = order.wishlist_item_total
        address = ShippingAddress.objects.filter(customer=customer)
       

        user_name= 0

        context= {'address': address, 'user_name': user_name, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items, 'order' : order}
        return render(request, 'web_project/checkout.html', context)
    else:  
        return redirect('login')
        


    
def store(request):
    products= Product.objects.all()

    if request.user.is_authenticated:
        products= Product.objects.all()
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total
        user_name = 0
    else: 
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']
        user_name= request.user


    context= {'user_name' : user_name, 'products': products, 'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
    return render(request, 'web_project/store.html', context)

def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('data:' , data)

    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['user form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.cart_total()):
            order.complete = True
        order.save()  
     

        if order.shipping() == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping data']['address'],
                city=data['shipping data']['city'],
                state=data['shipping data']['state'],
                zipcode=data['shipping data']['zipcode'],
              
            

            )
       

    else:
        print('user not logged in')



    return JsonResponse('payment submitted', safe=False)

def cart(request):
    #if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer 
    #using get_or_create function would either query the requested customer from database or create one if it does not exist. 
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems = order.wishlist_item_total
        user_name = 0


    #if user not authenticated
    else: 
        try:
            cart = json.loads(request.COOKIES['cart'])
            wishlist = json.loads(request.COOKIES['wishlist'])

        except:
            cart={}
            wishlist={}
        print('cart:', cart)
        print('wishlist:', wishlist)
        order_items=[]
        order={'cart_total':0, 'item_total':0, 'wishlist_item_total':0}
        cartItems = order['item_total']
        wishlistItems = order['wishlist_item_total']
        user_name= request.user


        # to update the cartitems icon for guest user 
        for cartitem in cart:
            cartItems += cart[cartitem]["quantity"]
            product = Product.objects.get(uniqueid = cartitem)
            total_price=(product.price * cart[cartitem]["quantity"])
            order['item_total'] += cart[cartitem]["quantity"]
            order['cart_total'] +=  total_price

            item = {
                'name' : {
                    'uniqueid' : product.uniqueid,
                    'name' : product.name,
                    'price' : product.price,
                    'imageurl' : product.imageurl,
                    'digital' : product.digital
                },
                'quantity' : cart[cartitem]["quantity"],
                'take_total' : total_price

            }
#adding each item in the dictionary order_items[]
            order_items.append(item)

            if product.digital == False:
                order['shipping'] = True

# to update the wishlistItems icon for guest user 
        for wishlistitem in wishlist:
            wishlistItems += wishlist[wishlistitem]["quantity"]

    context= {'user_name' : user_name, 'order_items':order_items, 'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems}
    return render(request, 'web_project/cart.html', context)

def wishlist(request):
    #if user is authenticated
    if request.user.is_authenticated:
        customer = request.user.customer 
    #using get_or_create function would either query the requested customer from database or create one if it does not exist. 
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtowishlist_set.all()
        wishlistItems = order.wishlist_item_total
        cartItems = order.item_total
        user_name=0


    #if user not authenticated
    else:
    #to prevent error when cart is empty we execute try and except method 
        try:
            cart = json.loads(request.COOKIES['cart'])
            wishlist = json.loads(request.COOKIES['wishlist'])

        except:
            cart={}
            wishlist={}
        
        print('cart:', cart)
        print('wishlist:', wishlist)
        order_items=[]
        order={'cart_total':0, 'item_total':0, 'wishlist_item_total':0, 'wishlist_total':0}
        cartItems = order['item_total']
        wishlistItems = order['wishlist_item_total']
        user_name = request.user 

        # to update the cartitems icon
        for cartitem in cart:
            cartItems += cart[cartitem]["quantity"]
        print('cartitems:', cartItems)

        # to update the wishlistItems icon
        for wishlistitem in wishlist:
            wishlistItems += wishlist[wishlistitem]["quantity"]
            product = Product.objects.get(uniqueid = wishlistitem)
            total_price=(product.price * wishlist[wishlistitem]["quantity"])
            order['wishlist_item_total'] += wishlist[wishlistitem]["quantity"]
            order['wishlist_total'] +=  total_price
            print('wishlistItems:', wishlistItems)

            item = {
                'name' : {
                    'uniqueid' : product.uniqueid,
                    'name' : product.name,
                    'price' : product.price,
                    'imageurl' : product.imageurl,
                },
                'quantity' : wishlist[wishlistitem]["quantity"],
                'take_total' : total_price

                }
#adding each item in the dictionary order_items[]
            order_items.append(item)
   

    context= {'user_name' : user_name, 'order_items':order_items, 'order': order, 'wishlistItems' : wishlistItems, 'cartItems' : cartItems}
    return render(request, 'web_project/wishlist.html', context)

#fetch product using its name 
def prod_view(request, name, uniqueid):
    product=Product.objects.get(name=name)
    unique_id=Product.objects.get(uniqueid=uniqueid)
    reviews= Reviews.objects.filter(name=unique_id)
    x=0
    for review in reviews:
        x += review.rate 
    rate_count=0
    if reviews.count()>0:
        rate_count=reviews.count()
        # to prevent error if there are no reviews on product page
    else: 
        rate_count = 1
        
    rate_average = x / rate_count

    if request.user.is_authenticated:
        product=Product.objects.get(name=name)
        unique_id=Product.objects.get(uniqueid=uniqueid)
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total
        user_name = 0 

    
    else:
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']
        rate_average = x / rate_count
        user_name = request.user 


     
    

    context= {'user_name': user_name, 'rate_average':  rate_average, 'product': product, 'reviews': reviews, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
    return render(request, 'web_project/productview.html', context)


def review(request, name, uniqueid):
    if request.user.is_authenticated:
        if request.method=="GET":
            product_id = request.GET.get('product_uniqueid')
            productid= Product.objects.get(uniqueid=product_id)
            review=request.GET.get('review')
            

            rate=request.GET.get('rate')
            if rate == None:
                rate=0
                return render(request, 'web_project/addrating.html')

        customer = request.user.customer
        Reviews(customer=customer, name=productid, review=review, rate=rate).save()
        return redirect('productview', name=name, uniqueid= uniqueid)

    else:
        print("please log in to review")

    return redirect('productview', name=name, uniqueid= uniqueid)




def movies(request):

    products= Movies.objects.all()
    if request.user.is_authenticated:
        products= Movies.objects.all()
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total
        user_name = 0 

    else: 
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']
        user_name = request.user 



    context= {'user_name': user_name, 'products': products, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
    return render(request, 'web_project/movies.html', context)
    


def books(request):
    products= Books.objects.all()

    if request.user.is_authenticated:
        products= Books.objects.all()
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total
        user_name = 0

    else: 
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']
        user_name = request.user 


    context= {'user_name': user_name, 'products': products, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
    return render(request, 'web_project/books.html', context)

def music(request):
    products= Music.objects.all() 
    if request.user.is_authenticated:
        products= Music.objects.all()
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total
        user_name = 0 

    else: 
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']
        user_name = request.user 



    context= {'user_name': user_name, 'products': products, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
    return render(request, 'web_project/music.html', context)
    

def updateaddtocart(request):
#converting a JSON string into an equivalent python object. This will help us see the data in the terminal too. 
    data = json.loads(request.body) 

    action = data['action']
    uniqueid=data['uniqueid']


    print('action:', action)
    print('uniqueid:', uniqueid)

    

#querying through all objects in Product using their respective names. using get_or_create and keeping status as false so that customer can keep adding product to the cart without any limits. 
    customer = request.user.customer 
    uniqueid= Product.objects.get(uniqueid=uniqueid)
    order, created = Order.objects.get_or_create(customer=customer, complete= False)
    order_items, created = Addtocart.objects.get_or_create(order=order, name=uniqueid)
  
    if action == 'add':
        order_items.quantity = (order_items.quantity + 1)
    elif action == 'remove':
        order_items.quantity = (order_items.quantity - 1)
    #for move to cart button in wishlist 
    elif action == 'add and remove':
        order_items.quantity = (order_items.quantity + 1)
    #for deleting item
    elif action == 'delete':
        order_items.quantity = 0
    
    order_items.save()


    if order_items.quantity <= 0:
        order_items.delete()

#this will be the response fetched once data is successfully processed when user adds item to cart. can see it in console. 
    return JsonResponse('item was added', safe=False)

def update_wishlist(request):
#converting a JSON string into an equivalent python object. This will help us see the data in the terminal too. 
    data = json.loads(request.body) 
    action = data['action']
    uniqueid=data['uniqueid']



    print('action:', action)
    print('uniqueid:', uniqueid)

    

#querying through all objects in Product using their respective names. using get_or_create and keeping status as false so that customer can keep adding product to the cart without any limits. 
    customer = request.user.customer 
    uniqueid= Product.objects.get(uniqueid=uniqueid)
    order, created = Order.objects.get_or_create(customer=customer, complete= False)
    order_items, created = Addtowishlist.objects.get_or_create(order=order, name=uniqueid)
    
    if action == 'add':
        order_items.quantity = (order_items.quantity + 1)
    elif action == 'remove':
        order_items.quantity = (order_items.quantity - 1)
    elif action == 'add and remove':
        order_items.quantity = (order_items.quantity - 1)
      #for deleting item
    elif action == 'delete':
        order_items.quantity = 0


    order_items.save()

    if order_items.quantity <= 0:
        order_items.delete()

    

#this will be the response fetched once data is successfully processed when user adds item to cart. can see it in console. 
    return JsonResponse('item was added', safe=False)

def search(request):
    if request.user.is_authenticated:
        products= Product.objects.all()
        customer = request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        order_items= order.addtocart_set.all()
        cartItems = order.item_total
        wishlistItems= order.wishlist_item_total

        if request.method == "GET":
            search = request.GET.get('search')
            if search:
                products = Product.objects.filter(Q(description__icontains=search)|Q(name__icontains=search)|Q(price__icontains=search)|Q(categoryname__icontains=search))
                context= {'products': products, 'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
                return render(request, 'web_project/search.html', context)
            else:
                print("search query does not exist")
                context= {'products': products, 'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
            return render(request, 'web_project/search.html', {})
    else: 
        cookieData = guest_cart(request)
        cartItems= cookieData['cartItems']
        order=cookieData['order']
        wishlistItems = cookieData['wishlistItems']
        order_items = cookieData['order_items']

        if request.method == "GET":
            search = request.GET.get('search')
            if search:
                products = Product.objects.filter(Q(description__icontains=search)|Q(name__icontains=search)|Q(price__icontains=search)|Q(categoryname__icontains=search))
                context= {'products': products, 'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
                return render(request, 'web_project/search.html', context)
            else:
                print("search query does not exist")
                context= {'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
                return render(request, 'web_project/search.html', {})

def user_profile(request):
    customer = request.user.customer
    name = customer.name 
    order, created= Order.objects.get_or_create(customer=customer, complete=False)
    orders = Order.objects.filter(customer=customer)
    order_items = Addtocart.objects.filter(order__in=orders)
    cartItems = order.item_total
    wishlistItems= order.wishlist_item_total
    context={'name': name, 'order_items': order_items, 'orders': orders, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems,}
    return render(request, 'web_project/user_profile.html', context)


def saved_address(request):

    customer = request.user.customer
    order, created= Order.objects.get_or_create(customer=customer, complete=False)
    orders = Order.objects.filter(customer=customer)
    cartItems = order.item_total
    wishlistItems= order.wishlist_item_total        
    
    if request.user.is_authenticated:
        customer = request.user.customer
        address = ShippingAddress.objects.filter(customer=customer)
         
     

    context={'address': address,'name': customer, 'orders': orders, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems,}

    return render(request, 'web_project/saved_address.html', context)
        
            

            
   











    