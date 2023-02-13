
from rest_framework import serializers
from products.models import Product

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

