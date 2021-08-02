from django.shortcuts import render

# Create your views here.
def buyer_home(request):
    return render(request,'buyer_home.html')
