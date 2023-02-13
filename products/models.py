# import uuid orderi deyish
from django.db import models
from core.models import AbstractModel
from django.contrib.auth.models import User
from slugify import slugify
from django.utils import translation
from django.db.models.signals import post_save 
from django.dispatch import receiver
from .helpers import send_sale_mail
import accounts.models
# Create your models here.


class ProductImg(AbstractModel):
    image=models.ImageField(upload_to='product_img')
    product=models.ForeignKey('Product',on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title 
    

class Category(AbstractModel):
    name=models.CharField(max_length=50)
    slug=models.SlugField(null=True, blank=True)
    parent_id=models.ForeignKey('self', null=True,blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.parent_id}-{self.name}'

    def get_absolute_url(self):
        if not self.parent_id:
            if translation.get_language()=='en':
                return f'/category/{self.slug}'
            else:
                return f'/{translation.get_language()}/category/{self.slug}'
                
        elif not self.parent_id.parent_id:
            if translation.get_language()=='en':
                return f'/category/{self.parent_id.slug}/{self.slug}'
            else:
                return f'/{translation.get_language()}/category/{self.parent_id.slug}/{self.slug}'
        elif not self.parent_id.parent_id.parent_id:
            if translation.get_language()=='en':
                return f'/category/{self.parent_id.parent_id.slug}/{self.parent_id.slug}/{self.slug}'
            else:
                return f'/{translation.get_language()}/category/{self.parent_id.parent_id.slug}/{self.parent_id.slug}/{self.slug}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Vendor(AbstractModel):
    name=models.CharField(max_length=50)
    star=models.IntegerField(null=True, blank=True)
    slug=models.SlugField(null=True, blank=True)
    fb=models.CharField(max_length=50, null=True, blank=True)
    gp=models.CharField(max_length=50, null=True, blank=True)
    tw=models.CharField(max_length=50, null=True, blank=True)
    ig=models.CharField(max_length=50, null=True, blank=True)
    vendor_desc=models.TextField()
    vendor_img=models.ImageField(upload_to="vendor_img")
    vendor_banner=models.ImageField(upload_to="vendor_img")

    def __str__(self):
        return self.name

    def get_stars(self):
        if self.star == None or self.star==False or self.star==0:
            stars = """
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 1:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 2:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 3:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 4:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 5:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            """
        return stars

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Vendor, self).save(*args, **kwargs)



class Product(AbstractModel):
    title=models.CharField(max_length=250)
    slug=models.SlugField(null=True, blank=True)
    desc=models.TextField()
    video=models.TextField()
    main_img=models.ImageField(upload_to="product_img")
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    price=models.FloatField(default=0.00)
    vendor=models.ForeignKey('Vendor',on_delete=models.CASCADE)
    discount_type=models.CharField(max_length=50, null=True, blank=True, choices=(('FAIZ' ,'Faiz'), ('QIYMET' , 'Qiymet')))
    discount_amount=models.FloatField(null=True, blank=True)
    actual_price=models.FloatField(null=True, blank=True)
    discount_time=models.DateTimeField(auto_now_add=False, null=True, blank=True)
    star=models.IntegerField(null=True, blank=True)
    property=models.ManyToManyField('PropertyValue', related_name='products', blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if not self.category.parent_id:
            if translation.get_language()=='en':
                return f"/product/{self.category.slug}/{self.slug}"
            else:
                return f"/{translation.get_language()}/product/{self.category.slug}/{self.slug}"
        elif not self.category.parent_id.parent_id:
            if translation.get_language()=='en':
                return f"/product/{self.category.parent_id.slug}/{self.category.slug}/{self.slug}"
            else:
                return f"/{translation.get_language()}/product/{self.category.parent_id.slug}/{self.category.slug}/{self.slug}"
        elif not self.category.parent_id.parent_id.parent_id:
            if translation.get_language()=='en':
                return f"/product/{self.category.parent_id.parent_id.slug}/{self.category.parent_id.slug}/{self.category.slug}/{self.slug}"
            else:
                return f"/{translation.get_language()}/product/{self.category.parent_id.parent_id.slug}/{self.category.parent_id.slug}/{self.category.slug}/{self.slug}"
   
    def get_stars(self):
        if self.star == None or self.star==False or self.star==0:
            stars = """
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 1:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 2:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 3:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 4:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 5:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            """
        return stars

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        exs = Product.objects.filter(slug=self.slug)
        if len(exs)>1:
            self.slug = f'{slugify(self.title)}-{self.id}'

        if self.discount_amount:
            if self.discount_type == 'FAIZ':
                self.actual_price=round(self.price-((self.price*self.discount_amount)/100),2)
                wishlists = accounts.models.WishList.objects.filter(product=self)
                if wishlists:
                    for wish in wishlists:
                        email = wish.user.email
                        product = wish.product
                        send_sale_mail(email, product)
                    
            elif self.discount_type == 'QIYMET':
                self.actual_price=round(self.price-self.discount_amount,2)
                wishlists = accounts.models.WishList.objects.filter(product=self)
                if wishlists:
                    for wish in wishlists:
                        email = wish.user.email
                        product = wish.product
                        send_sale_mail(email, product)
        else: 
            self.actual_price=round(self.price,2)
        super(Product, self).save(*args, **kwargs)

    

class Review(AbstractModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    star=models.IntegerField(null=True, blank=True)
    comment=models.TextField()
    product=models.ForeignKey('Product',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name}---{self.product.title}--{self.star}'

    def get_stars(self):
        if self.star == None or self.star==False or self.star==0:
            stars = """
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 1:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 2:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 3:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 4:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star"></span>
            """
        elif self.star == 5:
            stars = """
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            <span class="fa fa-star checked"></span>
            """
        return stars
class Property(AbstractModel):
    property=models.CharField(max_length=50)

    def __str__(self):
        return self.property

class PropertyValue(AbstractModel):
    values=models.CharField(max_length=50)
    property=models.ForeignKey('Property', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
    def __str__(self):
        return self.values


