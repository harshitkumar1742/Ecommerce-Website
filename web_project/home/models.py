from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="customer", null=True, blank=True)
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)
   

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=200, null=True, blank=True)
    # because product id changes for the same product when accessed on a different page, I have manually created a uniqueid for each product which will remain constant throughout. 
    uniqueid = models.CharField(max_length=10, null=True, blank= True)
    price=models.FloatField(default=0)
    digital=models.BooleanField(default=False, null=True, blank=True)
    categoryname=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)
    description=models.CharField(max_length=1000, null=True, blank= True)

    
    def __str__(self):
        return str(self.name)

    #in case there is no image url associated with the product, our server should not return an error. 
    def imageurl(self):
        try: 
            url=self.image.url
        except:
            url=''
        return url



class Order(models.Model):

    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True, blank=True)
    transaction_id=models.CharField(max_length=200, null=True)

    def __str__(self):  
        return str(self.customer)

    def shipping(self):
        shipping = False
        orderitems = self.addtocart_set.all()
        for item in orderitems:
            if item.name.digital == False:
                shipping = True   
               
        return shipping  

                
 

    def cart_total(self):
        total=0
        itemsordered = self.addtocart_set.all()
        for item in itemsordered:
            total +=item.take_total() 
        return total
    
    def item_total(self):
        total=0
        itemsordered = self.addtocart_set.all()
        for item in itemsordered:
            total +=item.quantity 
        return total

    def wishlist_item_total(self):
        total=0
        itemsordered = self.addtowishlist_set.all()
        for item in itemsordered:
            total +=item.quantity 
        return total

    def wishlist_total(self):
        total=0
        itemsordered = self.addtowishlist_set.all()
        for item in itemsordered:
            total +=item.take_total() 
        return total

class Addtocart(models.Model):

    name =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return str(self.order)


 #to dynamically change the total price of each product keeping quantity in mind in the add to cart page
    def take_total(self):
        total = self.name.price * self.quantity
        return total 


class Addtowishlist(models.Model):
    name=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return str(self.order)

 #to dynamically change the total price of each product keeping quantity in mind in the add to cart page
    def take_total(self):
        total = self.name.price * self.quantity
        return total 


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order=models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address=models.CharField(max_length=300, blank=True, null=True)
    city=models.CharField(max_length=300, blank=True, null=True)
    state=models.CharField(max_length=300, blank=True, null=True)
    zipcode=models.CharField(max_length=300, blank=True, null=True)
    date_added=models.DateTimeField(auto_now_add=True)

def __str__(self):  
    return str(self.customer) 


class Movies(models.Model):

    name =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price=models.FloatField()
    uniqueid = models.CharField(max_length=10, null=True, blank= True)
    digital=models.BooleanField(default=False, null=True, blank=True)
    categoryname=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)


    def __str__(self):
        return str(self.name)

    #in case there is no image url associated with the product, our server should not return an error. 
    def imageurl(self):
        try: 
            url=self.image.url
        except:
            url=''
        return url  


class Books(models.Model):
    name =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price=models.FloatField()
    uniqueid = models.CharField(max_length=10, null=True, blank= True)
    digital=models.BooleanField(default=False, null=True, blank=True)
    categoryname=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)

    
    def __str__(self):
        return str(self.name)

    #in case there is no image url associated with the product, our server should not return an error. 
    def imageurl(self):
        try: 
            url=self.image.url
        except:
            url=''
        return url 

class Music(models.Model):

    name =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price=models.FloatField()
    uniqueid = models.CharField(max_length=10, null=True, blank= True)
    digital=models.BooleanField(default=False, null=True, blank=True)
    categoryname=models.CharField(max_length=200, null=True, blank=True)
    image=models.ImageField(null=True, blank=True)


    def __str__(self):
        return str(self.name)

    #in case there is no image url associated with the product, our server should not return an error. 
    def imageurl(self):
        try: 
            url=self.image.url
        except:
            url=''
        return url  


class Reviews(models.Model):

    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    name =models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    review=models.TextField(max_length=250, null=True, blank=True)
    rate=models.IntegerField(default=0, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.name)

    
    def rate_total(self):
        total=0
        for rate in self.rate:
            total +=rate 
        return total
            
   

