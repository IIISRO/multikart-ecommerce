from django.db import models
from core.models import AbstractModel
from django.contrib.auth.models import User
from django.db.models.signals import post_save  
from django.dispatch import receiver
from products.models import Product

# Create your models here.




class Profile(AbstractModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, null=True, blank=True, default='')
    flat = models.CharField(max_length=50, null=True, blank=True, default='')
    address = models.CharField(max_length=100, null=True, blank=True, default='')
    zip = models.CharField(max_length=50, null=True, blank=True, default='')
    country = models.CharField(max_length=50, null=True, blank=True, default='')
    city = models.CharField(max_length=50, null=True, blank=True, default='')
    region = models.CharField(max_length=50, null=True, blank=True, default='')
    card = models.CharField(max_length=16, null=True, blank=True, default='')
    forget_pwd_token = models.CharField(max_length=100,null=True,blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = Profile.objects.create(user=kwargs['instance'])

    post_save.connect(create_profile, sender=User)
    
class WishList(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
class Subscriber(AbstractModel):
    email = models.EmailField()
    