from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def blog_home(request):
    return render(request, 'blog/blog_home.html')