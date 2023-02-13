from products.models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import viewsets, permissions


class ProductPage(APIView):
    permission_classes = (permissions.AllowAny,)
        
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug = self.kwargs.get('slug'))
        product_data = ProductSerializer(product).data
        categories = Category.objects.all()
        
        if not product.category.parent_id:
            get_object_or_404(categories, id=product.category.id, slug = self.kwargs.get('cat_slug'))
        elif not product.category.parent_id.parent_id:
            get_object_or_404(categories, id=product.category.id, slug = self.kwargs.get('cat_slug'))
            get_object_or_404(categories, id=product.category.parent_id.id, slug = self.kwargs.get('maincat_slug'))
        elif not product.category.parent_id.parent_id.parent_id:
            get_object_or_404(categories, id=product.category.id, slug = self.kwargs.get('cat_slug'))
            get_object_or_404(categories, id=product.category.parent_id.id, slug = self.kwargs.get('maincat_slug'))
            get_object_or_404(categories, id=product.category.parent_id.parent_id.id, slug = self.kwargs.get('mainmaincat_slug'))
        return Response(product_data)

class Products(APIView):
    http_method_names = ["get","post"]
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwags):
        products = Product.objects.all()
        products_list = ProductsSerializer(products, many = True).data
        return Response(products_list)

    def post(self, request):
        new_product = NewProductSerializer(data=request.data)
        if new_product.is_valid():
            new_product.save()
            return Response(new_product.data)
        return Response(new_product.errors)

class APICategoryPage(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self,*args,**kwargs):
        if self.kwargs.get('slug') and not self.kwargs.get('parent_slug') and not self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'))
            products = Product.objects.filter(category__parent_id__parent_id__slug=cat.slug)
            if self.request.GET.get('ordering', ""):
                if self.request.GET.get('ordering', "") == 'actual_price' or self.request.GET.get('ordering', "") == '-actual_price':
                    products = products.order_by(self.request.GET.get('ordering', ""))
                else:
                    raise Http404 
            if self.request.GET.get('vendor',''):
                if products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).exists():
                    products = products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).distinct() 
                else:
                    raise Http404
            if self.request.GET.get('color', ""):
                if products.filter(property__values__in = self.request.GET.get('color','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('color','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('size',''):
                if products.filter(property__values__in = self.request.GET.get('size','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('size','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('price',''):
                products = products.filter(actual_price__range = (self.request.GET.get('price','').split(";")[0],self.request.GET.get('price','').split(";")[1]))

            products_list = ProductsSerializer(products, many = True).data

        elif self.kwargs.get('slug') and self.kwargs.get('parent_slug') and not self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'), parent_id__slug=self.kwargs.get('parent_slug'))
            products = Product.objects.filter(category__parent_id__slug=cat.slug, category__parent_id__parent_id__slug=cat.parent_id.slug )

            if self.request.GET.get('ordering', ""):
                if self.request.GET.get('ordering', "") == 'actual_price' or self.request.GET.get('ordering', "") == '-actual_price':
                    products = products.order_by(self.request.GET.get('ordering', ""))
                else:
                    raise Http404 
            if self.request.GET.get('vendor',''):
                if products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).exists():
                    products = products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).distinct() 
                else:
                    raise Http404
            if self.request.GET.get('color', ""):
                if products.filter(property__values__in = self.request.GET.get('color','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('color','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('size',''):
                if products.filter(property__values__in = self.request.GET.get('size','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('size','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('price',''):
                products = products.filter(actual_price__range = (self.request.GET.get('price','').split(";")[0],self.request.GET.get('price','').split(";")[1]))

            products_list = ProductsSerializer(products, many = True).data

        elif self.kwargs.get('slug') and self.kwargs.get('parent_slug') and self.kwargs.get('maincat_slug'):
            cat = get_object_or_404(Category , slug = self.kwargs.get('slug'), parent_id__slug=self.kwargs.get('parent_slug'), parent_id__parent_id__slug=self.kwargs.get('maincat_slug'))
            products = Product.objects.filter(category__parent_id__parent_id__slug=cat.parent_id.parent_id.slug ,category__parent_id__slug=cat.parent_id.slug,category__slug=cat.slug)

            if self.request.GET.get('ordering', ""):
                if self.request.GET.get('ordering', "") == 'actual_price' or self.request.GET.get('ordering', "") == '-actual_price':
                    products = products.order_by(self.request.GET.get('ordering', ""))
                else:
                    raise Http404 
            if self.request.GET.get('vendor',''):
                if products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).exists():
                    products = products.filter(vendor__name__in = self.request.GET.get('vendor','').split("+")).distinct() 
                else:
                    raise Http404
            if self.request.GET.get('color', ""):
                if products.filter(property__values__in = self.request.GET.get('color','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('color','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('size',''):
                if products.filter(property__values__in = self.request.GET.get('size','').split("+")).exists():
                    products = products.filter(property__values__in = self.request.GET.get('size','').split("+")).distinct()
                else:
                    raise Http404
            if self.request.GET.get('price',''):
                products = products.filter(actual_price__range = (self.request.GET.get('price','').split(";")[0],self.request.GET.get('price','').split(";")[1]))

            products_list = ProductsSerializer(products, many = True).data
        return Response(products_list)