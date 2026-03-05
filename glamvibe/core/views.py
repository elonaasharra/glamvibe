from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from shop.models import Product
from django.db.models import Sum
from magazine.models import Post

def about(request):
    return render(request, 'core/about.html')
def contact(request):
    return render(request, 'core/contact.html')


def home(request):

    best_sellers = Product.objects.annotate(
        total_sold=Sum("order_items__quantity")
    ).order_by("-total_sold")[:8]

    most_popular = Post.objects.order_by(
        "-views",
        "-created_at"
    )[:4]

    return render(request, "core/home.html", {
        "best_sellers": best_sellers,
        "most_popular": most_popular
    })
