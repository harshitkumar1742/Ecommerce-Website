import json 
from .models import *

#purpose of this file is to handle the code we have created for guest users all at one place instead of repitition messing the structure in views.py.

def guest_cart(request):

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
                'take_total' : total_price,
                

            }
#adding each item in the dictionary order_items[]
        order_items.append(item)

        if product.digital == False:
            order['shipping'] = True
        


 #to update the wishlistItems icon for guest user 
    for wishlistitem in wishlist:
        wishlistItems += wishlist[wishlistitem]["quantity"]



    return {'order': order, 'cartItems' : cartItems, 'wishlistItems' : wishlistItems, 'order_items' : order_items}
