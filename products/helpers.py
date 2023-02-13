from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

def send_sale_mail(email, product):
    context ={
        "email":email,
        "product":product
    }
    html_content = render_to_string("sale-product.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        f"Hi. {product.title} from your Multikart wishlist is now on sale!",
        text_content,
        settings.EMAIL_HOST_USER ,
        [email]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True
