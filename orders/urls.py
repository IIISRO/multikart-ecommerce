from django.urls import path
from .views import *

app_name = 'orders'


urlpatterns=[
    path('cart/', cart,name='cart'),
    path('add-cart/', add_cart,name='add-cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/<slug:orderid>', order_success,name='order-success'),


]