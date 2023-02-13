from django.urls import path, re_path
from .views import *

app_name = 'accounts'

urlpatterns=[
    path('profile/', profile,name='profile'),
    path('login/', login_user,name='login'),
    path('logout/', logout_user,name='logout'),
    path('register/', register,name='register'),
    path('forget-pwd/', forget_pwd, name='forget-pwd'),
    path('change-pwd/<token>/', change_pwd, name='change-pwd'),
    path('add-wishlist/', add_wishlist, name='add-wishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('subscribe/', subscribe, name='subscribe'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    activate, name='activate'),

]

htmx_urlpatterns = [

]


urlpatterns += htmx_urlpatterns