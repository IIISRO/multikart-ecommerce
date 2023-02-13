from django import template
from products.models import Category

register = template.Library()

@register.simple_tag
def Nav():
    categories = Category.objects.all().order_by('created_at')
    return categories
