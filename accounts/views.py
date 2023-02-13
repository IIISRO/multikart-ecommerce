from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import json
from .models import Profile, WishList, Subscriber
from django.contrib import messages
from .helpers import send_forget_pwd,send_activate_link
from django.template.loader import get_template
from django.http import JsonResponse, HttpResponse,Http404
from django.utils.translation import gettext_lazy as _
import uuid
from social_django.models import UserSocialAuth
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str    
from products.models import Product
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
def forget_pwd(request):
    error = ''
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user and not user.social_auth.exists():
            username = User.objects.get(email=email).username
            user = User.objects.filter(username=username).first()
            token = str(uuid.uuid4())
            profile = Profile.objects.filter(user = user).first()
            profile.forget_pwd_token = token
            profile.save()
            messages.add_message(request, messages.SUCCESS, _("Password reset link sended your email!"))
            send_forget_pwd(user.email, token)
            return redirect(reverse_lazy('core:home'))
        else: error = _('This email not registred')
    return render(request,'forget_pwd.html', context={'error':error})

def change_pwd(request, token):
    get_object_or_404(Profile.objects.filter(forget_pwd_token = token))
    error = []
    profile = Profile.objects.get(forget_pwd_token = token)
    user = User.objects.filter(id=profile.user.id).first()
    if request.method == "POST":
        if len(request.POST['password']) < 3 and request.POST['password'] != request.POST['confirm_password']:
            error.append(_('Should Contain a minimum of 8 characters'))
            error.append(_('Not same password'))
        elif len(request.POST['password']) < 3:
            error.append(_('Should Contain a minimum of 8 characters'))
        elif request.POST['password'] != request.POST['confirm_password']:
            error.append(_('Not same password'))
        else:
            user.set_password(request.POST['password'])
            user.save()
            profile.forget_pwd_token=None
            profile.save()
            messages.add_message(request, messages.SUCCESS, _("Your password changed!"))
            return redirect(reverse_lazy('accounts:login'))
    return render(request, 'change_pwd.html', context={'error':error})

def login_user(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:profile'))
    else:
        error = ''
        if request.method == "POST":
            if '@' in request.POST['emailorusername']:
                email = request.POST['emailorusername']
                if User.objects.filter(email=email):
                    username = User.objects.get(email=email).username
                else: username=None
            else:
                username = request.POST['emailorusername']
                if User.objects.filter(username=username):
                    username = request.POST['emailorusername']
                else: username=None
            password = request.POST['password']
            user = authenticate(request, username = username, password = password)
            if user is not None: 
                login(request,user)
                if request.session.get('wishlist'):
                    wishlist=request.session['wishlist']
                    inWishlist = WishList.objects.filter(user=user)
                    for i in wishlist:
                        if not inWishlist.filter(product__id=i):
                            WishList.objects.create(user = user , product=Product.objects.get(id=i))
                    del request.session['wishlist']

                if request.GET.get('next'):
                    messages.add_message(request, messages.SUCCESS, f"{_('Welcome')} {str(username).upper()}!")
                    return redirect(request.GET.get('next'))
                else:
                    messages.add_message(request, messages.SUCCESS, f"{_('Welcome')} {str(username).upper()}!")
                    return redirect(reverse_lazy("accounts:profile"))
            # elif user.is_active=
            else:  error=_('Email or username or password wrong')
        return render(request,'login.html',  context={'error':error})

@login_required()
def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f"You're logout!")
    return redirect(reverse_lazy('core:home'))

    
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:profile'))
    else:
        form = RegistrationForm()
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                send_activate_link(user,current_site.domain,urlsafe_base64_encode(force_bytes(user.pk)), account_activation_token.make_token(user),)
                messages.add_message(request, messages.SUCCESS, f"Activation mail sended!")                
                return redirect(reverse_lazy('core:home'))
        return render(request,'register.html', context={'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and not user.is_active and account_activation_token.check_token(user, token)  :
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if request.session.get('wishlist'):
                    wishlist=request.session['wishlist']
                    inWishlist = WishList.objects.filter(user=user)
                    for i in wishlist:
                        if not inWishlist.filter(product__id=i):
                            WishList.objects.create(user = user , product=Product.objects.get(id=i))
                    del request.session['wishlist']
        messages.add_message(request, messages.SUCCESS, f"Welcome {(user.username).upper()}!")
        return redirect(reverse_lazy('accounts:profile'))
    else:
        raise Http404



@login_required()
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user' : user,
        'profile' : profile,
    }

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST['phone_number']
        flat = request.POST['flat']
        address = request.POST['address']
        zip = request.POST['zip']
        country = request.POST.get('country')
        city = request.POST['city']
        region = request.POST['region']
        if 'save' in request.POST:
            email_errors = []
            first_name_errors = []
            last_name_errors = []
            phone_number_errors = []
            city_errors = []
            region_errors = []
            username_errors = []
            if first_name != user.first_name and not user.social_auth.exists():
                if not first_name.isalpha():
                    first_name_errors.append(_('Worng first name'))
                else: 
                    user.first_name = first_name

            if last_name != user.last_name and not user.social_auth.exists():
                if not last_name.isalpha():
                    last_name_errors.append(_('Worng last name'))
                else: 
                    user.last_name = last_name

            if username != user.username:
                if User.objects.filter(username=username):
                    username_errors.append(_('This username already exists'))
                elif '@' in username:
                    username_errors.append(_('You cannot use @ in username'))
                else:
                    user.username = username

            if email != user.email and not user.social_auth.exists():
                if User.objects.filter(email=email):
                    email_errors.append(_('This email already exists'))
                else:
                    user.email = email

            if phone_number != profile.phone_number:
                if not phone_number.isdigit() or len(phone_number)<10:
                    phone_number_errors.append(_('Wrong phone number'))
                else:
                    profile.phone_number = phone_number

            if flat != profile.flat: 
                profile.flat = flat

            if address != profile.address:
                profile.address = address

            if zip != profile.zip:
                profile.zip = zip

            if country != profile.country and country != None:
                profile.country = country

            if city != profile.city:
                if not (city.replace(' ','')).isalpha():
                    city_errors.append(_('Wrong type'))
                else:
                    profile.city = city

            if region != profile.region:
                if not (region.replace(' ','')).isalpha():
                    region_errors.append(_('Wrong type'))
                else:
                    profile.region = region

            user.save()
            profile.save()

            context = {
            'user' : user,
            'profile' : profile,
            'email_errors' : email_errors,
            'username_errors' : username_errors,
            'first_name_errors' : first_name_errors ,
            'last_name_errors' : last_name_errors,
            'phone_number_errors' : phone_number_errors,
            'city_errors' : city_errors,
            'region_errors' : region_errors
            }
        else:
            if first_name != user.first_name:
                return HttpResponse('')
            elif last_name != user.last_name:              
                return HttpResponse('')
            elif email != user.email:         
                return HttpResponse('')
            elif username != user.username:         
                return HttpResponse('')
            elif phone_number != profile.phone_number:              
                return HttpResponse('')
            elif flat != profile.flat:
                return HttpResponse('')
            elif address != profile.address:
                return HttpResponse('')
            elif zip != profile.zip:
                return HttpResponse('')
            elif country != profile.country:
                return HttpResponse('')
            elif city != profile.city:
                return HttpResponse('')
            elif region != profile.region:
                return HttpResponse('')
            else:
                return HttpResponse('<a style="position: absolute; background-color: #fd7164; background-image: none; color: white; border-color: #fd7164;" class="btn btn-sm btn-solid">Save setting</a>')

        


    return render(request,'profile.html', context)

def wishlist(request):
    return render(request,'wishlist.html')

def add_wishlist(request):
    if request.method == 'GET':
        raise Http404
    data = json.loads(request.body)
    if not data:
        raise Http404
    action = data['action']
    productId = data['productId']
    userId = data['userId']

    if request.user.is_authenticated:
        inWishlist = WishList.objects.filter(user=userId)
        if action=='add':
            if not inWishlist.filter(product=productId):
                WishList.objects.create(user = User.objects.get(id=userId) , product=Product.objects.get(id=productId))
        elif action=='remove':
            if inWishlist.filter(product=productId):
                inWishlist.get(product=productId).delete()

    else:
        if request.session.get('wishlist'):
            inWishlist = request.session.get('wishlist')
        else:
            request.session['wishlist']=[]
            inWishlist = request.session.get('wishlist')
        if action=='add':
            if not productId in inWishlist:
                inWishlist.append(productId)
                request.session['wishlist']=inWishlist
                
        elif action=='remove':
            if productId in inWishlist:
                inWishlist.remove(productId)
                request.session['wishlist']=inWishlist
    
    return JsonResponse(' ', safe=False)

def subscribe(request):
    if request.method == 'GET':
        raise Http404
    data = json.loads(request.body)
    if not data:
        raise Http404
    
    email=data['email']
    if not Subscriber.objects.filter(email=email):
        Subscriber.objects.create(email = email)
        return JsonResponse('ok', safe=False)
    else:
        return JsonResponse('exists', safe=False)
    


