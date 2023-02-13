from django.urls import path
from .views import *


app_name = 'products_api'

urlpatterns = [
    path('products/', Products.as_view(), name = 'products'),
    path('product/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='apiproduct1'),
    path('product/<slug:maincat_slug>/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='apiproduct2'),
    path('product/<slug:mainmaincat_slug>/<slug:maincat_slug>/<slug:cat_slug>/<slug:slug>/', ProductPage.as_view(), name='apiproduct3'),
    path('category/<slug:slug>/',APICategoryPage.as_view(), name='apicategorypg1'),
    path('category/<slug:parent_slug>/<slug:slug>/',APICategoryPage.as_view(), name='apicategorypg2'),
    path('category/<slug:maincat_slug>/<slug:parent_slug>/<slug:slug>/',APICategoryPage.as_view(), name='apicategorypg3'),

    

]