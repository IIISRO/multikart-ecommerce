from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin
# Register your models here.


# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(Vendor)
admin.site.register(ProductImg)
# admin.site.register(Review)
# admin.site.register(Property)
# admin.site.register(PropertyValue)

class Imginlines(admin.TabularInline):
    model = ProductImg

@admin.register(Category)
class CategorySearch(TranslationAdmin, admin.ModelAdmin,):
    search_fields = ['name']

@admin.register(Vendor)
class vendor(admin.ModelAdmin):
    search_fields = ['name']
    exclude = ('star',)

    
@admin.register(Review)
class review(admin.ModelAdmin):
    search_fields = ['user']

@admin.register(Property)
class property(admin.ModelAdmin):
    search_fields = ['property']

@admin.register(PropertyValue)
class propertyvalue(admin.ModelAdmin):
    search_fields = ['values']

@admin.register(Product)
class product(admin.ModelAdmin):
    search_fields = ['title']
    exclude = ('star',)
    inlines = [ Imginlines, ]

        