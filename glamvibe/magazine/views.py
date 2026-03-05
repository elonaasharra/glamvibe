from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator


def magazine_home(request):

    posts_list = Post.objects.order_by("-views", "-created_at")

    paginator = Paginator(posts_list, 6)  # 6 artikuj për faqe
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    return render(request, "magazine/magazine_home.html", {
        "posts": posts
    })


def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)

    # rrit views çdo herë që hapet artikulli
    post.views += 1
    post.save()

    return render(request, "magazine/post_detail.html", {
        "post": post
    })