from rest_framework import serializers
from products.models import *

class ProductPropertyValueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PropertyValue
        fields = ( 'id','property_id','values') 

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImg
        fields = ( 'image','product') 

class ProductsSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    stars = serializers.SerializerMethodField()
    property = ProductPropertyValueSerializer(many=True)
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ( 
            'id',
            'title',
            'desc',
            'video',
            'main_img',
            'category',
            'price',
            'vendor',
            'discount_type',
            'discount_amount',
            'actual_price',
            'discount_time',
            'stars',
            'property',
            'url'
        )
    def get_vendor(self, obj):
        return {'name':obj.vendor.name,'slug':obj.vendor.slug}
    def get_category(self, obj):
        return {'id':obj.category.id,'name':obj.category.name}
    def get_url(self,  obj):
        return obj.get_absolute_url()
    def get_stars(self,obj):
        return obj.get_stars()

class ProductSerializer(serializers.ModelSerializer):


    img = serializers.SerializerMethodField()
    vendor_categories = serializers.SerializerMethodField()
    vendor = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    property = ProductPropertyValueSerializer(many=True)
    category = serializers.SerializerMethodField()
    new_products = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()


    class Meta:
        model = Product
        fields = (
            'title',
            'desc',
            'video',
            'main_img',
            'category',
            'price',
            'vendor',
            'discount_type',
            'discount_amount',
            'discount_time',
            'star',
            'property',
            'img',
            'vendor_categories',
            'related_products',
            'new_products',
            'detail',
            'url'
        )
    
    def get_img(self, obj):
        img = ProductImageSerializer(ProductImg.objects.filter(product=obj.id),many=True).data
        return img

    def get_vendor(self, obj):
        return {'name':obj.vendor.name,'slug':obj.vendor.slug}

    def get_category(self, obj):
        return {'id':obj.category.id,'name':obj.category.name}

    def get_vendor_categories(self, obj):
        categories = Category.objects.all()
        products = Product.objects.all()
        
        vendor_categories = {}

        for i in categories:
            for j in products:
                if j.vendor_id == obj.vendor.id:
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
                                vendor_categories[i.name]=i.name.slug
        return vendor_categories

    def get_related_products(self,obj):
        related_products = ProductsSerializer(Product.objects.filter(category_id=obj.category_id)[:30], many=True).data
        return related_products

    def get_new_products(self, obj):
        new_products = ProductsSerializer(Product.objects.order_by("-created_at")[:30], many=True).data
        return new_products

    def get_detail(self, obj):     
        property = Property.objects.all()
        propertyvalue = obj.property.all()
        detail = {}
      
        for i in property:
            detailpropertyvalues=[]
            for j in propertyvalue:
                if j.property_id == i.id:
                    detailpropertyvalues.append(j)
                    detail[str(i)]=(','.join(map(str,detailpropertyvalues)))
    
        return detail

    def get_url(self,  obj):
        return obj.get_absolute_url()

class NewProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            'desc',
            'video',
            'main_img',
            'category',
            'price',
            'vendor',
            'property'
            )
 
