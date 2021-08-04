from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import pickle
import os
from .models import city, Property, Seller
from xgboost import XGBRegressor
import numpy as np
with open('seller_app/model_pickle', 'rb') as f:
    model = pickle.load(f)
    # print(ob)

def predict(area,bhk,resale,rera_approved, c):
    c = city.objects.get(name = c.lower())
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
        City = request.POST.get('city')
        state = request.POST.get('state')
        type_of_house = request.POST.get('type_of_house')  # BHK OR RK
        bhk = request.POST.get('bhk')  # no of Bedrooms
        resale = request.POST.get('resale')  # yes , no
        rera_approved = request.POST.get('rera')  # yes , no
        proposed_price = request.POST.get('p_price')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')
        predicted_price = predict(area, bhk, resale, rera_approved, City)
        price_per_share = 1e5
        print(predicted_price)

        max_no_of_shares = finalized_price(float(proposed_price), predicted_price)/price_per_share
        p = Property(area=area,address= address,
                     city=City, state=state, resale=resale,
                     bhk = int(bhk) if bhk != '' else 0,
                     rera_approved= rera_approved, prop_image= image,
                     max_no_of_shares = max_no_of_shares,
                     no_of_shares =0,
                     price_per_share = price_per_share,
                     predicted_price=finalized_price(float(proposed_price), predicted_price),

                    )
        p.save()
        seller = Seller( seller_details = request.user, proposed_price=proposed_price, property_details= p )
        seller.save()

        return render(request, 'sell.html',{'success': "Your Response has been recorded, We'll reach out to you soon!"})
    else:
        return render(request, 'sell.html')
