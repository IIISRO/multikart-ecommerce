from orders.models import Cart
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import viewsets, permissions

class CartApi(APIView):
    http_method_names = ["get","post"]
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwags):
        

        if request.user.is_authenticated:
            cart_products = Cart.objects.filter(user=request.user)
        

        products_list = CartProductsSerializer(cart_products, many = True).data
        return Response(products_list)
