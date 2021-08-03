from django.shortcuts import render,redirect

# Create your views here.
def seller_home(request):
    return render(request,'seller_home.html')

def sell_form(request):
    if request.method == 'POST':

        # values to be saved in DB.
        name = request.POST.get('name')
        image = request.FILES['image']
        address = request.POST.get('address')
        area = request.POST.get('area')
        city = request.POST.get('city')
        state = request.POST.get('state')
        type_of_house = request.POST.get('type_of_house') # BHK OR RK
        bhk = request.POST.get('bhk') # no of Bedrooms
        resale = request.POST.get('resale') # yes , no
        rera_approved = request.POST.get('rera') # yes , no
        proposed_price = request.POST.get('p_price')
        phone_number = request.POST.get('number')
        email = request.POST.get('email')


        return render(request,'sell.html',{'success':"Your Response has been recorded, We'll reach out to you soon!"})
    else:
        return render(request,'sell.html')
