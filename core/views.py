from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from products.models import Product, Vendor
import json
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q  
from django.core import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import WishList

# Create your views here.

def home(request):
    top_collection=Product.objects.filter(star=5)
    vendors = Vendor.objects.all()
    new_products=Product.objects.all().order_by('created_at')[:8]
    top_sellers=Product.objects.filter(vendor__star__range=[4,5])
    if request.user.is_authenticated:
        wishlist=WishList.objects.filter(user=request.user)
        wishlist_id=[]
        for i in wishlist:
            wishlist_id.append(i.product.id)
    else:
        wishlist_id=[]
        if request.session.get('wishlist'):
            for i in request.session['wishlist']:
                wishlist_id.append(int(i))
        
        
    return render(request,'index.html',context={'top_collection':top_collection,'new_products':new_products,'top_sellers':top_sellers,'wishlist':wishlist_id,'vendors':vendors})

def error_404_view(request, exception):
    return render(request,'404.html')

def about_page(request):
    return render(request,'about-page.html')

class Contact(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, _("Thanks. We will contact soon!"))
        return super().form_valid(form)

def faq(request):
    return render(request,'faq.html')

def search(request):
    search = request.GET.get('search', "")
    if search:
        product = Product.objects.filter(Q(title__icontains=search)|Q(vendor__name__icontains=search))[:6] 
                                                                                                         

    else:
        product = []

    if request.user.is_authenticated:
        wishlist=WishList.objects.filter(user=request.user)
        wishlist_id=[]
        for i in wishlist:
            wishlist_id.append(i.product.id)
    else:
        wishlist_id=[]
        if request.session.get('wishlist'):
            for i in request.session['wishlist']:
                wishlist_id.append(int(i))

    context={
        'product':product,
        'wishlist':wishlist_id
    }
    return render(request,'search.html', context)

def autosuggestApi(request):
    if 'term' in request.GET:
        search = request.GET.get('term')
        qs = Product.objects.filter(Q(title__icontains=search))[:10]
        titles = []
        href = []
        for product in qs:
            titles.append((product.title).capitalize())
            href.append((product.slug).capitalize())


    return JsonResponse(titles, safe=False)         