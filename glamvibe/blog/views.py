from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def blog_home(request):
    posts = BlogPost.objects.all().order_by('-created_at')

    return render(request, 'blog/blog_home.html', {
        'posts': posts
    })

def blog_post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def create_post(request):

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = post.title.replace(" ", "-").lower()
            post.save()

            return redirect("blog:blog_home")

    else:
        form = BlogPostForm()

    return render(request, "blog/create_post.html", {"form": form})


from django.http import JsonResponse

@login_required
def like_post(request, slug):

    post = get_object_or_404(BlogPost, slug=slug)

    liked = False

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)

        if post.likes > 0:
            post.likes -= 1

    else:
        post.liked_by.add(request.user)
        post.likes += 1
        liked = True

    post.save()

    return JsonResponse({
        "likes": post.likes,
        "liked": liked
    })