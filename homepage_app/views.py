from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def index(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        signup = request.POST.get('signup')

        if login:
            return redirect('Login')
        else:
            return redirect('Signup')

    else:
        return render(request, 'homepage.html')

def signup(request):
    signup = {'title':'Signup','navigate':'Signup'}

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 == pass2:
             try:
                user = User.objects.get(username = request.POST['username']) # to check if user exists
                return render(request,'login_signup.html',{'title':'Signup','navigate':'Signup','error':'WARNING ! Username Already Exist,Choose A Different Username.'})

             except User.DoesNotExist:
                 user = User.objects.create_user(username,password = pass1)
                 auth.login(request,user) # to login
                 return redirect('home')
    else:
        return render(request,'login_signup.html',signup)

def login(request):
    login = {'title':'Login','navigate':'Login'}

    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        user = auth.authenticate(username = username,password = pass1)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'login_signup.html',{'title':'Login','navigate':'Login','error':'Username or password wrong!!!'})

    else:
        return render(request,'login_signup.html',login)
