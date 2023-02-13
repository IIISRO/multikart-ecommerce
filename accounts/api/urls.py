from django.urls import path
from .views import WishListApi


app_name = 'accounts_api'

urlpatterns = [
    path('wishlist/', WishListApi.as_view(), name = 'wishlist_api'),

]