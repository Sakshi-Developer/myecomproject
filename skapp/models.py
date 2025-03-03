from django.db import models
from django.contrib.auth.models import User

class Enquiry(models.Model):
    username= models.CharField(max_length= 255)
    email= models.CharField(max_length= 255, null=True)
    contact= models.CharField(max_length=20)
    message= models.TextField(null=True)
    enq_date= models.DateField(auto_now_add= True, editable=True)

    def __str__(self):
        return self.username
    

class Support(models.Model):
    username= models.CharField(max_length= 255)
    email= models.EmailField()
    contact= models.CharField(max_length= 20)
    service= models.CharField(max_length= 50)
    message= models.TextField(null=True)
    calling_date= models.DateField(auto_now_add=True, editable=True) 

    def __str__(self):
        return self.username
    

    


class Product(models.Model):
    code=models.CharField(max_length=100)
    title= models.CharField(max_length=255)
    name= models.CharField(max_length=100)
    mrp= models.CharField(max_length=100)
    gst= models.FloatField()
    discription= models.TextField()
    stock= models.IntegerField()
    image= models.ImageField()
    category= models.ForeignKey('Category', on_delete= models.CASCADE)
    

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField()   

    def __str__(self):
        return self.name


class Slider(models.Model):
    name= models.CharField(max_length= 100)
    image= models.ImageField()

    def __str__(self):
        return self.name
    
class cartModel(models.Model):
    userid= models.ForeignKey(User, on_delete= models.CASCADE)
    pid= models.ForeignKey(Product, on_delete= models.CASCADE)
    qty= models.IntegerField(default=1)
    cart_date= models.DateField(auto_now_add= True, editable= True)


    def __str__(self):
        return str(self.userid)
    

class Order(models.Model):
    userid= models.ForeignKey(User, on_delete= models.CASCADE)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    contact= models.CharField(max_length=50)
    email= models.EmailField()
    country=models.CharField(max_length=255)
    state=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    pincode= models.IntegerField()
    address= models.TextField()
    orderamt= models.FloatField(null=True)
    payment_mode=models.CharField(max_length=100)
    trackingno=models.CharField(max_length=100, null=True)
    order_date= models.DateTimeField(auto_now_add=True)
    order_status=(
            ("pending", "Pending"),
            ("confirm", "Confirm"),
            ("deliver", "Deliver"),
            ("cancel", "Canceled"),
            ("return", "Return"),
            ("refund", "Refund")
        )
    order_status=models.CharField(max_length=100, choices= order_status, default="pending")

    def __str__(self):
        return "Order From {name}".format(name=self.first_name)


class OrderItems(models.Model):
    userid= models.ForeignKey(User, on_delete=models.CASCADE)
    productid= models.ForeignKey(Product, on_delete= models.CASCADE)
    orderid= models.CharField(max_length=100, null=True)
    orderdate= models.DateField(auto_now_add=True, null=True)
    order_qty=models.IntegerField()

    def __str__(self):
        return "Order Items in Order ID {order}".format(order=self.orderid) 
    

class country(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class state(models.Model):
    name=models.CharField(max_length=100)
    cid= models.ForeignKey(country, on_delete= models.CASCADE)

    def __str__(self):
        return self.name


class city(models.Model):
    name=models.CharField(max_length=100)
    sid= models.ForeignKey(state, on_delete= models.CASCADE)

    def __str__(self):
        return self.name

class orderTracking(models.Model):
    trackingid= models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    productid=  models.ForeignKey(Product, on_delete=models.CASCADE)
    message= models.TextField()
    status_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.trackingid.orderid











    




    


    

    




