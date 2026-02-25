from django.urls import path
from . import views

app_name = 'magazine'

urlpatterns = [
    path('', views.magazine_home, name='magazine_home'),
]