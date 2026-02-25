from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def magazine_home(request):
    return render(request, 'magazine/magazine_home.html')