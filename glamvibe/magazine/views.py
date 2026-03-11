from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.core.paginator import Paginator


def magazine_home(request):

    category_slug = request.GET.get("category")

    posts_list = Post.objects.order_by("-views", "-created_at")

    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)

    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, "magazine/magazine_home.html", {
        "posts": posts,
        "categories": categories
    })
def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)

    # rrit views çdo herë që hapet artikulli
    post.views += 1
    post.save()

    return render(request, "magazine/post_detail.html", {
        "post": post
    })