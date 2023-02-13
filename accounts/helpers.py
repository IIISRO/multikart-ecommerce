from django.core.mail import send_mail
from django.conf import settings

def send_forget_pwd(email,token):
    subject = 'Reset your password'
    message = f'Hi, click here and reset your MULTIKART account password "http://localhost/account/change-pwd/{token}/"' 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_activate_link(user,domain,uid,token):
    subject = 'Activate your account'
    html_content = render_to_string('activation_email.html', {
    'user': user,
    'domain': domain,
    'uid':uid,
    'token': token,
    })
    text_content = strip_tags(html_content)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject,text_content, email_from, recipient_list)
    return True






def send_sub_mail(email, products):
    context ={
        "email":email,
        "products":products
    }
    html_content = render_to_string("email-subscribers.html", context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        "Hi. Welcome our this week's best rated products!",
        text_content,
        settings.EMAIL_HOST_USER ,
        [email]
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return True


