import razorpay
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from seller_app.models import *
from .models import *


# Create your views here.


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@csrf_exempt
@require_http_methods([ "POST"])
def buyed_share(request,prop_id, buy_shares):
    if request.method == "POST":
        if 'razorpay_payment_id' in request.POST:
            # get the required parameters from post request.
            payment_id = request.POST['razorpay_payment_id']
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            amount = razorpay_client.order.fetch(razorpay_order_id)['amount']
            # print(amount)# Rs. 200
            signature = request.POST.get('razorpay_signature', '')
            buyer_data = {'prop_id': prop_id, 'buy_share': buy_shares, 'money': amount}
            prop = Property.objects.get(id=buyer_data['prop_id'])
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                try:

                    # capture the payemt
                    # capturing is not needed as we have turned on auto capture
                    # razorpay_client.payment.capture(payment_id, amount)


                    #The below if else is not needed as razorpay handles it
                    # if prop.price_per_share * int(buyer_data['buy_share']) != float(buyer_data['buy_share']):
                        # print("Locho Che")
                    # else:

                    prop.no_of_shares -= int(buyer_data['buy_share'])
                    prop.save()
                    obj = Buyer.objects.create(
                        buyer_details=User.objects.get(pk=request.user.id),
                        buyer_property=prop,
                        buyer_shares=int(buyer_data['buy_share']),
                        buyer_order_id = razorpay_order_id
                    )
                    obj.save()

                    # render success page on successful capture of payment
                    return redirect(f'/buyer/payment_success/{obj.id}')
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment.
                    return redirect(f'payment_failure/p{prop_id}/{buy_shares}/{razorpay_order_id}')
            else:
                print('here2')
                # if signature verification fails.
                return redirect(f'payment_failure/{prop_id}/{buy_shares}/{razorpay_order_id}')
        else:
            # There is an error
            error = request.POST.get('error')
            print(error)
        return redirect(f'payment_failure/{prop_id}/{buy_shares}/{razorpay_order_id}')
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


@login_required(login_url='/login')
@require_http_methods(['GET', 'POST'] )
def buy(request,id):
    if(request.method == 'GET'):
        prop = Property.objects.filter(id=id)
        return render(request,'buy.html',{'prop':prop[0]})
    else:
        currency = 'INR'
        prop_id = int(request.POST.get('prop_id'))
        prop = Property.objects.get(id=request.POST.get('prop_id'))
        no_of_shares = int(request.POST.get('no_of_shares'))
        amount = prop.price_per_share * no_of_shares * 100  #Since the amount should be in paisa
        print(amount)
        if amount > 5*1e5*1e2:
            return HttpResponseBadRequest()
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           ))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/buyer/buy_success/' + str(prop_id) + '/' + str(no_of_shares)

        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['prefill'] = {'name': request.user.username}
        context['prop'] = prop
        return render(request, 'buy.html', context)

@login_required(login_url='/login')
def buyer_home(request):
    list_of_prop = Property.objects.filter(no_of_shares__gt = 0, approved =True,property_active=True ).exclude( seller__seller_details = request.user )
    return render(request, 'buyer_home.html',{'list':list_of_prop})


@login_required(login_url='/login')
def payment_success(request, buyer_id):
    buyer = Buyer.objects.get( id=buyer_id )
    if buyer.buyer_details != request.user:
        return HttpResponse('Not authorized', status= 401)
    return render( request, 'payment_success.html', {'buyer': buyer, 'prop': buyer.buyer_property} )

def payment_failure(request, prop_id, buy_shares, order_id):
    prop = Property.objects.get(id=prop_id)
    # order= razorpay_client.order.fetch(order_id)
    payments = requests.get(f'https://api.razorpay.com/v1/orders/{order_id}/payments')
    errors = [x['error_description'] for x in payments.content.items]
    return render(request, 'payment_failure', {'prop': prop, 'no_of_shares': buy_shares, 'errors': errors})