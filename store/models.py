from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import CharField



class Customer(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , blank=True , null=True)
    name = models.CharField(max_length=200 , null=True)
    email = models.CharField(max_length=200 , null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200 , null=True)
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    image = models.ImageField(upload_to='images/product' , null=True , blank=True)
    digital = models.BooleanField(default=False , null=True , blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/static/images/empty.jpg'
        return url

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.SET_NULL , blank=True , null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False , null=True , blank=False)
    transection_id = models.CharField(max_length=200 , null=True)

    @property
    def get_cart_total(self):
        total = 0
        for order_item in self.orderitem_set.all():
            total += order_item.get_product_total
        return total

    @property
    def shipping(self):
        shipping = False
        check_digital = self.orderitem_set.filter(product__digital=False).exists()
        if check_digital:
            shipping = True
            return shipping
        else:
            return shipping

    @property
    def get_order_item_count(self):
        return self.orderitem_set.count()
    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.SET_NULL , null=True)
    order = models.ForeignKey(Order , models.SET_NULL , null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return str(self.product.name)

    @property
    def get_product_total(self):
        total_price = self.product.price * self.quantity
        return total_price

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer , on_delete=models.SET_NULL , null=True)
    order = models.ForeignKey(Order , on_delete=models.SET_NULL , null=True)
    address = models.CharField(max_length=300 , null=False)
    city = models.CharField(max_length=300 , null=False)
    state = models.CharField(max_length=300 , null=False)
    zipcode = models.CharField(max_length=300 , null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address