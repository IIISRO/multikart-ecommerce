from django.urls import path
from .views import *

app_name = 'products'


urlpatterns=[
    path('vendors/<slug:slug>/', VendorPage.as_view(), name='vendors'),
    path('product/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='product1'),
    path('product/<slug:maincat_slug>/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='product2'),
    path('product/<slug:mainmaincat_slug>/<slug:maincat_slug>/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='product3'),
    path('category/<slug:slug>/',CategoryPage.as_view(), name='categorypg1'),
    path('category/<slug:parent_slug>/<slug:slug>/',CategoryPage.as_view(), name='categorypg2'),
    path('category/<slug:maincat_slug>/<slug:parent_slug>/<slug:slug>/',CategoryPage.as_view(), name='categorypg3'),

]
