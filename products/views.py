from django.shortcuts import render, get_object_or_404,HttpResponse,redirect
from django.views.generic import DetailView, ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import *
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
import math
from accounts.models import WishList
from django.http import Http404

# from datetime import datetime, timedelta



# Create your views here.

class VendorPage(DetailView):
    model = Vendor
    context_object_name = 'none'
    template_name = 'vendor-profile.html'
    def get_context_data(self, **kwargs):
        get_object_or_404(Vendor, slug=self.kwargs.get('slug'))
        context = super(VendorPage, self).get_context_data(**kwargs)
        vendor = Vendor.objects.get(slug=self.kwargs.get('slug'))
        prod = Product.objects.filter(vendor=vendor.id).order_by("-created_at")
        categories = Category.objects.all()
        propertyvalues = PropertyValue.objects.all()

        vendor_categories = [] 

        for i in categories:
            for j in prod:
                if i.id == j.category_id:
                    if i.parent_id: 
                        if i.parent_id.parent_id:
                            if i.parent_id.parent_id.name not in vendor_categories:
                                vendor_categories.append(i.parent_id.parent_id.name)
                        else:
                            if i.parent_id.name not in vendor_categories:
                                vendor_categories.append(i.parent_id.name)
                    else:
                        if i.name not in vendor_categories:
                            vendor_categories.append(i.name)
      
        vendor_colors = {}
   
        for i in prod:
            for j in i.property.all():
                if j.property_id == 2:
                    if j.id not in vendor_colors:
                        vendor_colors[j.id] = j.values

                        
        ordering = self.request.GET.get('ordering', "")
        sort_color = self.request.GET.get('color', "")

        if sort_color:
            prod = prod.filter(property = sort_color)

        if ordering:
            prod = prod.order_by(ordering)
    
        product_per_page=6

        page = self.request.GET.get('page', 1)
        product_paginator = Paginator(prod, product_per_page)
        try:
            prod = product_paginator.page(page)
        except EmptyPage:
            prod = product_paginator.page(product_paginator.num_pages)
        except:
            prod = product_paginator.page(product_per_page)

        if product_paginator.num_pages > 1:
            is_paginated = True
        else:
            is_paginated=False

        context['reviews'] = Review.objects.filter(product__in=prod)
        context['vendor'] = vendor
        context['prod'] = prod
        context['vendor_categories'] = vendor_categories
        context['is_paginated'] = is_paginated
        context['paginator'] = product_paginator
        context['page_obj'] = prod
        context['propertyvalues'] = propertyvalues
        context['vendor_colors'] = vendor_colors

        return context



class ProductPage(DetailView):
    context_object_name = 'products'
    model = Product
    template_name = 'product-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prod = get_object_or_404(Product, slug = self.kwargs.get('slug'))
        categories = Category.objects.all()
        if not prod.category.parent_id:
            get_object_or_404(categories, id=prod.category.id, slug = self.kwargs.get('cat_slug'))
        elif not prod.category.parent_id.parent_id:
            get_object_or_404(categories, id=prod.category.id, slug = self.kwargs.get('cat_slug'))
            get_object_or_404(categories, id=prod.category.parent_id.id, slug = self.kwargs.get('maincat_slug'))
        elif not prod.category.parent_id.parent_id.parent_id:
            get_object_or_404(categories, id=prod.category.id, slug = self.kwargs.get('cat_slug'))
            get_object_or_404(categories, id=prod.category.parent_id.id, slug = self.kwargs.get('maincat_slug'))
            get_object_or_404(categories, id=prod.category.parent_id.parent_id.id, slug = self.kwargs.get('mainmaincat_slug'))

        new_products = Product.objects.order_by("-created_at")[:30]
        related_products = Product.objects.filter(category_id=prod.category_id)[:30]
        products = Product.objects.all()
        property = Property.objects.all()
        propertyvalue = prod.property.all()
        vendor = Vendor.objects.get(id=prod.vendor_id)
        detail = {}
      
        for i in property:
            detailpropertyvalues=[]
            for j in propertyvalue:
                if j.property_id == i.id:
                    detailpropertyvalues.append(j)
                    detail[i]=(','.join(map(str,detailpropertyvalues)))
    
        vendor_categories = {}

        for i in categories:
            for j in products:
                if j.vendor_id == vendor.id:
                    if i.id == j.category_id:
                        if i.parent_id: 
                            if i.parent_id.parent_id:
                                if i.parent_id.parent_id.name not in vendor_categories:
                                    vendor_categories[i.parent_id.parent_id.name]=i.parent_id.parent_id.slug
                            else:
                                if i.parent_id.name not in vendor_categories:
                                    vendor_categories[i.parent_id.name]=i.parent_id.slug
                        else:
                            if i.name not in vendor_categories:
                                vendor_categories[i.name]=i.slug

       
        if self.request.user.is_authenticated:
            wishlist=WishList.objects.filter(user=self.request.user)
            wishlist_id=[]
            for i in wishlist:
                wishlist_id.append(i.product.id)
        else:
            wishlist_id=[]
            if self.request.session.get('wishlist'):
                for i in self.request.session['wishlist']:
                    wishlist_id.append(int(i))  
        context['wishlist']=wishlist_id
        context['reviews'] = Review.objects.filter(product=prod)
        context['prod'] = prod     
        context["img"] = ProductImg.objects.filter(product=prod.id)     
        context['vendor'] = vendor
        context['vendor_categories'] = vendor_categories
        context["property"] = property
        context["detail"] = detail
        context['related_products'] = related_products
        context['new_products'] = new_products
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('star') and request.POST.get('comment') and 'save' in request.POST:
            Review.objects.create(user=request.user,star=request.POST.get('star'),product=Product.objects.get(slug=self.kwargs.get('slug')),comment=request.POST.get('comment'))
            prod=Product.objects.get(slug=self.kwargs.get('slug'))
            all_review = Review.objects.filter(product=prod)
            stars=int()
            for i in all_review:
                stars+=int(i.star)
            stars=stars/len(all_review)
            prod.star=math.ceil(stars)
            prod.save()

            products = Product.objects.filter(vendor=prod.vendor)
            stars=int()
            ct=int()
            for i in products:
                if i.star:
                    ct+=1
                    stars+=int(i.star)
            stars=stars/ct
            vendor = Vendor.objects.get(id=prod.vendor.id)
            vendor.star=math.ceil(stars)
            vendor.save()

            messages.add_message(request, messages.SUCCESS, "Thanks for comment!")
            return redirect(prod.get_absolute_url())

        if (request.POST.get('star') and request.POST.get('comment')):
            return HttpResponse('<button name="save" class="btn btn-solid" style="padding:15px;" type="submit">Submit Your Review</button>')

        else:
            return HttpResponse('<button class="btn" disabled style="cursor:default; background-color: #ff4c3b; color: white;padding: 15px;" type="submit">Submit Your Review</button>')
class CategoryPage(TemplateView):
    template_name = 'category-page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get('slug') and not self.kwargs.get('parent_slug') and not self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'))
            product = Product.objects.filter(category__parent_id__parent_id__slug=cat.slug)
            if not product:
                raise Http404

        elif self.kwargs.get('slug') and self.kwargs.get('parent_slug') and not self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'), parent_id__slug=self.kwargs.get('parent_slug'))
            product = Product.objects.filter(category__parent_id__slug=cat.slug, category__parent_id__parent_id__slug=cat.parent_id.slug )
            if not product:
                raise Http404

        elif self.kwargs.get('slug') and self.kwargs.get('parent_slug') and self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'), parent_id__slug=self.kwargs.get('parent_slug'), parent_id__parent_id__slug=self.kwargs.get('maincat_slug'))
            product = Product.objects.filter(category__parent_id__parent_id__slug=cat.parent_id.parent_id.slug ,category__parent_id__slug=cat.parent_id.slug,category__slug=cat.slug)
            if not product:
                raise Http404
       
        if self.request.user.is_authenticated:
            wishlist=WishList.objects.filter(user=self.request.user)
            wishlist_id=[]
            for i in wishlist:
                wishlist_id.append(i.product.id)
        else:
            wishlist_id=[]
            if self.request.session.get('wishlist'):
                for i in self.request.session['wishlist']:
                    wishlist_id.append(int(i)) 

        vendors=[]
        colors=[]
        sizes=[]
        for i in product:
            if i.vendor.name not in vendors:
                vendors.append(i.vendor.name)
            for j in i.property.all():
                if j.property_id == 2:
                    if j.values not in colors:
                        colors.append(j.values)
                elif j.property_id == 5:
                    if j.values not in sizes:
                        sizes.append(j.values)



                
        context['cat']=cat
        context['vendors'] = vendors
        context['colors'] = colors
        context['sizes']=sizes
        context['new_products']=Product.objects.all().order_by('-created_at')
        context['wishlist']=("" . join([str(a) for a in wishlist_id]))
        return context
    
