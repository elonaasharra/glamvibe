from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_home(request):
    posts = BlogPost.objects.all().order_by('-created_at')

    return render(request, 'blog/blog_home.html', {
        'posts': posts
    })

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})