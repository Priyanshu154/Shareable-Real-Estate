import json
from datetime import date, datetime, timedelta
import random

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
from buyer_app.models import *
from homepage_app.handle_transactions import make_transaction
from homepage_app.models import Person
from seller_app.models import *
import requests


def setup_account(person,year,month,day):
    # making account holder
    url = settings.ZETA_BASE_URL + "/applications/newIndividual"
    headers = settings.HEADERS
    data = json.dumps({
        "ifiID": settings.IFI_ID,
        "individualType": "REAL",
        "formID": f"daemons_thread_{random.randint(1,1e8)}",
        "firstName": person.first_name,
        "lastName":person.last_name,
        "dob": {
            "year": year,
            "month": month,
            "day": day,
        },
        "gender": person.gender,
        "kycDetails": {
            "kycStatus": "MINIMAL",
            "authData": {
                "PAN": person.pan
            },
            "authType": "PAN"
        },
        "vectors": [
            {
                "type": "p",
                "value": "+91"+person.mobile_no,
                "isVerified": "true"
            }
        ]
    })

    response = requests.post(url,data = data,headers = headers).json()
    print(response)
    holder_id = response['individualID']

    # Making bundle
    url = settings.ZETA_BASE_URL + f"/bundles/{settings.BUNDLE_ID}/issueBundle"
    data = json.dumps(
        {
            "accountHolderID": holder_id,
            "name": "Shareable Real Estate Bundle",
            "phoneNumber": "+91" + person.mobile_no,
            "requestID": f"{person.first_name}-{person.last_name}-{person.pan}-{random.randint(1,1e5)}"
        }
    )
    bundle = requests.post(url, data=data, headers = headers).json()
    print(bundle)
    account_id = bundle['accounts'][0]['accountID']

    # transaction

    # url = settings.ZETA_BASE_URL + "/transfers"
    # data = json.dumps({
    #     "requestID": f"{person.first_name}-{person.last_name}-{person.pan}-{random.randint(1,1e5)}",
    #     "amount": {
    #         "currency": "INR",
    #         "amount": 50000
    #     },
    #     "transferCode": "ATLAS_P2M_AUTH",
    #     "debitAccountID": settings.ADMIN_ACCOUNT_ID,
    #     "creditAccountID": account_id,
    #     "transferTime": 1574741608000,
    #     "remarks": "Share-able Real-Estate Initial Pay.",
    # })
    #
    # res = requests.post(url,data=data,headers=headers)
    # print(res.json())
    res = make_transaction( debitID=settings.ADMIN_ACCOUNT_ID, creditID= account_id, amount=50000 )
    print(res)
    return holder_id, account_id



def index(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        signup = request.POST.get('signup')
        buyer = request.POST.get('buyer')
        seller = request.POST.get('seller')

        if login:
            return redirect('Login')
        elif signup:
            return redirect('Signup')
        elif buyer:
            return redirect('buyer')
        elif seller:
            return redirect('seller')

    else:
        prop = Property.objects.all()

        for i in prop:
            if ((i.property_date + timedelta(days=365)) == date.today() ) and (
                    i.property_active == True):
                print("Yes")
                i.property_active = False
                interest = [10, 15, 20]
                irate = random.choice(interest) #Interest Rate
                i.sold_price = (i.actual_price * (100 + irate)) / 100  ##This is the sold price of prop and we have to increment it in admin bank account
                ## transfer to admin from funding
                i.save()
                res = make_transaction(debitID= settings.FUNDING_ID, creditID = settings.ADMIN_ACCOUNT_ID,
                                       amount= i.sold_price)
            else:
                print("NO" + str(i.id))

        buyers = Buyer.objects.filter(Q(buyer_active = True),Q(buyer_property__property_active = False))
        for b in buyers:
            if (b.buyer_date + timedelta(days=365)) == date.today() :
                print("buyer " , b.id)
                irate = ((b.buyer_property.sold_price - b.buyer_property.actual_price)/b.buyer_property.actual_price)*100
                buyer_rupees = ((b.buyer_shares * b.buyer_property.price_per_share) * (100 + irate - 2)) / 100
                print("irate", irate)
                print("buyer_rupees = ",buyer_rupees)
                ## Transfer buyer_rupees to buyer from admin
                res = make_transaction( debitID= settings.ADMIN_ACCOUNT_ID, creditID = Person.objects.get(user = b.buyer_details).account_id,
                                        amount = buyer_rupees)

                b.buyer_active = False
                b.save()

        return render(request, 'homepage.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    signup = {'title': 'Signup', 'navigate': 'Signup', 'opposite': 'Login'}

    if request.method == 'POST':
        username = request.POST.get('username').strip()
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        dob = request.POST.get('dob').strip()
        pan = request.POST.get('pan').strip()
        mobile = request.POST.get('mobile').strip()
        gender = request.POST.get('gender').strip()
        first = request.POST.get('first').strip()
        last = request.POST.get('last').strip()

        if dob and pan and mobile and gender and first and last:
            if pass1 == pass2:
                try:
                    user = User.objects.get(username=request.POST['username'])  # to check if user exists
                    return render(request, 'login_signup.html', {'title': 'Signup', 'navigate': 'Signup',
                                                                 'error': 'WARNING ! Username Already Exist,Choose A Different Username.',
                                                                 'opposite': 'Login'})

                except User.DoesNotExist:
                    user = User.objects.create_user(username, password=pass1)
                    p = Person()
                    p.user = user
                    p.first_name = first
                    p.last_name = last
                    p.pan = pan
                    p.dob = dob
                    p.gender = gender
                    p.mobile_no = mobile
                    account_holder_id,account_id = setup_account(p,dob.split('-')[0], dob.split('-')[1]  ,dob.split('-')[2])
                    p.account_holder_id = account_holder_id
                    p.account_id = account_id

                    p.save()
                    auth.login(request, user)  # to login
                    return redirect('home')
            else:
                return render(request, 'login_signup.html',
                              {'title': 'Signup', 'navigate': 'Signup', 'error': 'WARNING ! Passwords Dont Match.',
                           'opposite': 'Login'})
        else:
            return render(request, 'login_signup.html', {'title': 'Signup', 'navigate': 'Signup',
                                                                 'error': 'WARNING ! Enter All Fields!',
                                                                 'opposite': 'Login'})
    else:
        return render(request, 'login_signup.html', signup)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    login = {'title': 'Login', 'navigate': 'Login', 'opposite': 'Signup'}

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = auth.authenticate(username=username, password=pass1)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login_signup.html',
                          {'title': 'Login', 'navigate': 'Login', 'error': 'WARNING ! Username or password wrong!!!',
                           'opposite': 'Signup'})

    else:
        return render(request, 'login_signup.html', login)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')


@login_required(login_url='/login')
def profile(request):
    buyer = Buyer.objects.filter(buyer_details=request.user)
    seller = Seller.objects.filter(seller_details=request.user)
    user = request.user
    person =  Person.objects.get(user = user)
    url = settings.ZETA_BASE_URL+f"/accounts/{person.account_id}/balance"
    res = requests.get(url,headers=settings.HEADERS).json()
    balance = res['balance']
    return render(request, 'profile.html', {'buyer': buyer, 'seller': seller,'balance':balance})
