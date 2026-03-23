from django.urls import path
from . import views
from .views import subscribe

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('subscribe/', subscribe, name='subscribe'),

]