from django.shortcuts import render,redirect,get_list_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy , reverse
from django.contrib.auth import get_user_model
import json
from accounts.models import Profile
from django.http import JsonResponse, Http404, HttpResponse
from .models import Cart, Orders
from products.models import Product, PropertyValue
from django.db.models import Q
from django.conf import settings
import stripe
import random
from datetime import timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()
# Create your views here.
@login_required()
def cart(request):
    return render(request,'cart.html')






import stripe
stripe.api_key = "sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"



 



@login_required()
def checkout(request):

    context={}


    if request.GET.get('prod', ""):
        user = request.user
        profile = Profile.objects.get(user=request.user)
        products = get_list_or_404(Product , slug=request.GET.get('prod',''))[0]
        amount=products.actual_price * int(request.GET.get('quantity',""))
        if request.method == "POST":
            amount = float(products.actual_price) 
            #Create customer
            try:
                customer = stripe.Customer.create(
                            email=request.user.email,
                            name=request.user.first_name,
                            description="Product payment",
                            source=request.POST['stripeToken']
                            )

            except stripe.error.CardError as e:
                return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))     

            except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

            except stripe.error.InvalidRequestError as e:
                return HttpResponse("<h1>Invalid requestor!</h1>")

            except stripe.error.AuthenticationError as e:  
                return HttpResponse("<h1>Invalid API auth!</h1>")

            except stripe.error.StripeError as e:  
                return HttpResponse("<h1>Stripe error!</h1>")

            except Exception as e:  
                pass  
            #Stripe charge 
            charge = stripe.Charge.create(
                    customer=customer,
                        amount=int(products.actual_price)*100,
                        currency='usd',
                        description="Product selling"
                    ) 
            transRetrive = stripe.Charge.retrieve(
                        charge["id"],
                        api_key="sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"
                    )
            charge.save() # Uses the same API Key.

            while True:
                orderId=random.randint(0,100000000)
                if not Orders.objects.filter(orderId=orderId):
                    orderId=random.randint(0,100000000)
                    break

            order = Orders.objects.create(product = products, orderId=orderId, quantity=request.GET.get('quantity',''), first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),email=request.POST.get('email'),phone_number=request.POST.get('phone_number'),
                                        flat=request.POST.get('flat'),address=request.POST.get('address'),zip=request.POST.get('zip'),country=request.POST.get('country',f"{profile.country}"),
                                        city=request.POST.get('city'),region=request.POST.get('region'),payed=amount
            )
            order.save()
            return redirect(f'/orders/order-success/{orderId}')





        
        context={
            'user':user,
            'profile':profile,
            'products':products,
            'amount':amount,
            'quantity':request.GET.get('quantity',""),
            'incart':False
        }
    else:
        user = request.user
        profile = Profile.objects.get(user=request.user)
        products = Cart.objects.filter(user=request.user)
        if request.method == "POST":
            amount = float(request.POST.get('amount')) 
            #Create customer
            try:
                customer = stripe.Customer.create(
                            email=request.POST.get('email'),
                            name=request.POST.get('first_name'),
                            description="Product payment",
                            source=request.POST['stripeToken']
                            )

            except stripe.error.CardError as e:
                return HttpResponse("<h1>There was an error charging your card:</h1>"+str(e))     

            except stripe.error.RateLimitError as e:
                    # handle this e, which could be stripe related, or more generic
                    return HttpResponse("<h1>Rate error!</h1>")

            except stripe.error.InvalidRequestError as e:
                return HttpResponse("<h1>Invalid requestor!</h1>")

            except stripe.error.AuthenticationError as e:  
                return HttpResponse("<h1>Invalid API auth!</h1>")

            except stripe.error.StripeError as e:  
                return HttpResponse("<h1>Stripe error!</h1>")

            except Exception as e:  
                pass  
            #Stripe charge 
            charge = stripe.Charge.create(
                    customer=customer,
                        amount=int(amount)*100,
                        currency='usd',
                        description="Product selling"
                    ) 
            transRetrive = stripe.Charge.retrieve(
                        charge["id"],
                        api_key="sk_test_51MT1tpIpI2DRrDde4li8UJBGaNS73zugCRBzco8SHT71xKHy2byY41Aogmnt33dEbAJDWqTAfPs5d5MVTNsCBTcH00Xfdxda1D"
                    )
            charge.save() # Uses the same API Key.
            while True:
                    orderId=random.randint(0,100000000)
                    if not Orders.objects.filter(orderId=orderId):
                        orderId=random.randint(0,100000000)
                        break
            for i in products:
                order = Orders.objects.create(product = i.product, orderId=orderId, quantity=i.quantity, first_name=request.POST.get('first_name'),
                                            last_name=request.POST.get('last_name'),email=request.POST.get('email'),phone_number=request.POST.get('phone_number'),
                                            flat=request.POST.get('flat'),address=request.POST.get('address'),zip=request.POST.get('zip'),country=request.POST.get('country',f"{profile.country}"),
                                            city=request.POST.get('city'),region=request.POST.get('region'),payed=amount    
                )
                i.delete()
            order.save()
            return redirect(f'/orders/order-success/{orderId}')


        
        amount=float()
        
        for i in products:
            amount+=i.total_price
        context={
            'user':user,
            'profile':profile,
            'products':products,
            'amount':round(amount,2),
            'incart':True
        }

    return render(request,'checkout.html', context)






@login_required()
def order_success(request,orderid):
    orders=Orders.objects.filter(orderId=orderid)
    if orders[0].is_success==False:
        context={}
        country=orders[0].country
        city=orders[0].city
        region=orders[0].region
        flat=orders[0].flat
        address=orders[0].address
        zip=orders[0].zip
        phone_number=orders[0].phone_number
        order_date=orders[0].created_at 
        delivery_date=order_date + timedelta(days=30)
        payed=float(round(orders[0].payed,2))

        context['orders']=orders
        context['orderid']=orders[0].orderId
        context['country']=country
        context['city']=city
        context['region']=region
        context['flat']=flat
        context['address']=address
        context['zip']=zip
        context['phone_number']=phone_number
        context['order_date']=order_date.strftime('%d %B %Y')
        context['delivery_date']=delivery_date.strftime('%d %B %Y')
        context['payed']=payed

        for i in orders:
            i.is_success=True
            i.save()
        

        return render(request,'order-success.html',context)
    else:
        raise Http404

@login_required()    
def add_cart(request):
    if request.method == 'GET':
        raise Http404
    data = json.loads(request.body)
    if not data:
        raise Http404
    action = data['action']
    productId = data['productId']
    quantity = data['quantity']
    size = data['size']
    color = data['color']
    userId = data['userId']
    cart=Cart.objects.filter(user=userId,product=productId,property__values=color.replace(' ',''))
    cart = cart.filter(property__values=size).first()
    if action=='add':
        if not cart:
            cart = Cart.objects.create(user = User.objects.get(id=userId), product=Product.objects.get(id=productId), quantity=quantity)
            cart.property.add(PropertyValue.objects.get(values=size))
            cart.property.add(PropertyValue.objects.get(values=color.replace(' ','')))
            cart.save()
        else:
            cart.quantity+=int(quantity)
            cart.save()
    elif action=='remove':
        if cart:
            cart.delete()     
    elif action=='update':
        if cart:
            cart.quantity=int(quantity)
            cart.save()
  

    return JsonResponse(' ', safe=False)