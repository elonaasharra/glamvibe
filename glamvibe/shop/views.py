from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def shop_home(request):
    return render(request, 'shop/shop_home.html')