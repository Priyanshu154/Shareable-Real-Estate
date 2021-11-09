from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import pickle
import os
from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

from real_estate_project import settings
from .models import city, Property, Seller
from xgboost import XGBRegressor
import numpy as np
with open('seller_app/model_pickle', 'rb') as f:
    model = pickle.load(f)
    # print(ob)

def predict(area,bhk,resale,rera_approved, c):
    c = city.objects.get(name = c)
    features = np.array([[
        float(area), float(bhk) if bhk != '' else 1, 0 if bhk != '' else 1, int(resale), int(rera_approved),
        c.latitude, c.longitude
    ]])
    return float(model.predict(features)[0])*1e5

def finalized_price( proposed, predicted ):
    if (abs(proposed-predicted)/proposed)*100  <= 10:
        return min(proposed, predicted)
    else:
        return proposed



# Create your views here.
@login_required(login_url='/login')
def seller_home(request):
    return render(request, 'seller_home.html')


@login_required(login_url='/login')
def sell_form(request):
    if request.method == 'POST':

        # values to be saved in DB.
        name = request.POST.get('name')
        image = request.FILES['image']
        address = request.POST.get('address')
        area = request.POST.get('area')
        City = request.POST.get('actual_city')
        print(request.POST.get('nearest_city'))
        nearest_city = city.objects.get(id= request.POST.get('nearest_city'))
        state = request.POST.get('state')
        type_of_house = request.POST.get('type_of_house')  # BHK OR RK
        bhk = request.POST.get('bhk')  # no of Bedrooms
        resale = request.POST.get('resale')  # yes , no
        rera_approved = request.POST.get('rera')  # yes , no
        proposed_price = request.POST.get('p_price')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')
        predicted_price = predict(area, bhk, resale, rera_approved, nearest_city.name)
        price_per_share = 1e5
        print(predicted_price)

        max_no_of_shares = finalized_price(float(proposed_price), predicted_price)/price_per_share
        p = Property(area=area,address= address,
                     city=City, state=state, resale=resale,
                     bhk = int(bhk) if bhk != '' else 0,
                     rera_approved= rera_approved, prop_image= image,
                     max_no_of_shares = max_no_of_shares,
                     no_of_shares =max_no_of_shares,
                     price_per_share = price_per_share,
                     predicted_price=finalized_price(float(proposed_price), predicted_price),
                    nearest_city = nearest_city
                    )
        p.save()
        seller = Seller( seller_details = request.user, proposed_price=proposed_price, property_details= p )
        seller.save()

        return render(request, 'sell.html',{'success': "Your Response has been recorded, We'll reach out to you soon!"})
    else:

        cities = city.objects.all().order_by('name')
        return render(request, 'sell.html', {'cities': cities})

@login_required(login_url='/login')
@require_http_methods( ['GET', 'POST']  )
def approve_property(request,id):
    if request.method=='GET':
        prop = Property.objects.get(id=id)
        return render(request, 'approve.html', {'prop': prop})
    else:
        response = request.POST.get('response',False)
        prop = Property.objects.get(id=id)
        if response == "False":
            prop.delete()
            return redirect('home')
        else:
            prop.approved = True
            prop.actual_price = prop.predicted_price
            prop.save()
            return render(request,'approve.html', {'prop': prop,'status': True})
