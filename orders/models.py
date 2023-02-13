from django.db import models
from core.models import *
from django.contrib.auth.models import User
from products.models import Product, PropertyValue,Property
# Create your models here.


class Cart(AbstractModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    property=models.ManyToManyField(PropertyValue, related_name='carts')
    quantity=models.IntegerField()
    total_price = models.FloatField()

    def __str__(self):
        return f'{self.user}---{self.product}---{self.quantity}'

    def save(self, *args, **kwargs):
        self.total_price=round(float(self.product.actual_price) * int(self.quantity),2)
        super(Cart, self).save(*args, **kwargs)

class Orders(AbstractModel):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    orderId=models.IntegerField(unique=False)
    quantity=models.IntegerField()
    first_name = models.CharField(max_length=50, null=True, blank=True, default='')
    last_name = models.CharField(max_length=50, null=True, blank=True, default='')
    email = models.CharField(max_length=50, null=True, blank=True, default='')      
    phone_number = models.CharField(max_length=50, null=True, blank=True, default='')
    flat = models.CharField(max_length=50, null=True, blank=True, default='')
    address = models.CharField(max_length=100, null=True, blank=True, default='')
    zip = models.CharField(max_length=50, null=True, blank=True, default='')
    country = models.CharField(max_length=50, null=True, blank=True, default='')
    city = models.CharField(max_length=50, null=True, blank=True, default='')
    region = models.CharField(max_length=50, null=True, blank=True, default='')
    payed = models.IntegerField()
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product}---{self.orderId}---{self.first_name} {self.last_name}'