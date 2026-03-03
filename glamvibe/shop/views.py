from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product


def shop_home(request):
    products = Product.objects.all()  # marrim të gjitha produktet
    return render(request, 'shop/shop_home.html', {
        'products': products
    })