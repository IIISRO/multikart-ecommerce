from celery import shared_task
from .helpers import send_sub_mail
from .models import Subscriber
from products.models import Product
# celery -A multicart worker --beat --scheduler django --loglevel=info  
@shared_task
def send_mail():
    for i in Subscriber.objects.all():
        email=i.email
        product=Product.objects.filter(star=5)[:3]
        send_sub_mail(email,product)