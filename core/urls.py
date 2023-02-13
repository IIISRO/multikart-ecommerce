from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('',home,name='home'),
    path('about-page/',about_page,name='aboutus'),
    path('contact/', Contact.as_view() ,name='contact'),
    path('faq/',faq,name='faq'),
    path('search/',search,name='search'),
    path('autosuggestApi/', autosuggestApi ,name='autosuggestApi'),

]