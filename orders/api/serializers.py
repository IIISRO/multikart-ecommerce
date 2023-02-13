
from rest_framework import serializers
from products.models import Product,PropertyValue
from orders.models import Cart

class ProductPropertyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyValue
        fields = ('values',) 



class ProductsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ( 
            'id',
            'title',
            'main_img',
            'actual_price',
            'url'
        )
    def get_url(self,  obj):
        return obj.get_absolute_url()


class CartProductsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    property = ProductPropertyValueSerializer(many=True)

    
    class Meta:
        model = Cart
        fields = ( 
            'user',
            'product',
            'property',
            'quantity',
            'total_price'

        )




    def get_product(self,obj):
        product = ProductsSerializer(Product.objects.filter(id=self.product.id, many=True)).data
        return product    
