from accounts.models import WishList
from products.models import Product
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response

class WishListApi(APIView):
    http_method_names = ["get","post"]
    def get(self, request, *args, **kwags):
        

        if request.user.is_authenticated:
            wish_products = WishList.objects.filter(user=request.user)
            products = []
            for product in wish_products:
                products.append(product.product)
        else:
            wishlist_id=[]
            if request.session.get('wishlist'):
                for i in request.session['wishlist']:
                    wishlist_id.append(int(i))
            products=Product.objects.filter(id__in=wishlist_id).distinct()

        

        products_list = ProductsSerializer(products, many = True).data
        return Response(products_list)
