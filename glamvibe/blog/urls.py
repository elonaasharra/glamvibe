from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_home, name='blog_home'),
    path('post/<slug:slug>/', views.blog_post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('like/<slug:slug>/', views.like_post, name='like_post'),
]