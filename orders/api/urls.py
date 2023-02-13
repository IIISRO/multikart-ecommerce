from django.urls import path
from .views import CartApi


app_name = 'orders_api'

urlpatterns = [
    path('cart/', CartApi.as_view(), name = 'cart_api'),
]