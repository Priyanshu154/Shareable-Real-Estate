from datetime import date, datetime, timedelta
import random

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
from buyer_app.models import *
from seller_app.models import *


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
            if ((i.property_date + timedelta(days=365)) == date.today()) and (
                    i.property_active == True and i.approved == True):
                print("Yes")
                i.property_active = False
                interest = [10, 15, 20]
                irate = random.choice(interest)
                i.sold_price = (i.actual_price * (100 + irate)) / 100  ##This is the sold price of prop and we have to increment it in admin bank account
                ## transfer to admin from funding
                i.save()
            else:
                print("NO")

        buyers = Buyer.objects.filter(Q(buyer_active = True),Q(buyer_property__property_active = False))
        for b in buyers:
            if (b.buyer_date + timedelta(days=365)) == date.today() :
                irate = ((b.buyer_property.sold_price - b.buyer_property.actual_price)/b.buyer_property.actual_price)*100
                buyer_rupees = ((b.buyer_shares * b.buyer_property.price_per_share) * (100 + irate - 2)) / 100
                print("buyer_rupees = ",buyer_rupees)
                ## Transfer buyer_rupees to buyer from admin
                b.buyer_active = False
                b.save()

        return render(request, 'homepage.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    signup = {'title': 'Signup', 'navigate': 'Signup', 'opposite': 'Login'}

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
            try:
                user = User.objects.get(username=request.POST['username'])  # to check if user exists
                return render(request, 'login_signup.html', {'title': 'Signup', 'navigate': 'Signup',
                                                             'error': 'WARNING ! Username Already Exist,Choose A Different Username.',
                                                             'opposite': 'Login'})

            except User.DoesNotExist:
                user = User.objects.create_user(username, password=pass1)
                auth.login(request, user)  # to login
                return redirect('home')
        else:
            return render(request, 'login_signup.html',
                          {'title': 'Signup', 'navigate': 'Signup', 'error': 'WARNING ! Passwords Dont Match.',
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

    return render(request, 'profile.html', {'buyer': buyer, 'seller': seller})
