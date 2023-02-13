from django import template
register = template.Library()

@register.simple_tag
def discount(type,price,sale):
    if type == "FAIZ":
        sale = (price * sale) / 100
        price = price - sale
    elif type == "QIYMET":
        price = price - sale
    return ('%.2f' % price)