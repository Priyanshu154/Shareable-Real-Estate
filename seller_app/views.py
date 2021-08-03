from django.shortcuts import render,redirect

# Create your views here.
def seller_home(request):
    return render(request,'seller_home.html')

def sell_form(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'sell.html')
