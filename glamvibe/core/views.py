
# Create your views here.
import re
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from shop.models import Product
from django.db.models import Sum
from magazine.models import Post
from blog.models import BlogPost
from .models import ContactMessage
from .models import Subscriber

def about(request):
    return render(request, 'core/about.html')

def home(request):

    best_sellers = Product.objects.annotate(
        total_sold=Sum("order_items__quantity")
    ).order_by("-total_sold")[:8]

    most_popular = Post.objects.order_by(
        "-views",
        "-created_at"
    )[:4]

    featured_opinion = BlogPost.objects.order_by('-likes').first()
    side_opinions = BlogPost.objects.order_by('-likes')[1:3]

    return render(request, "core/home.html", {
        "best_sellers": best_sellers,
        "most_popular": most_popular,
        "featured_opinion": featured_opinion,
        "side_opinions": side_opinions,
    })


def contact_view(request):

    if request.method == "POST":

        name = request.POST.get("name").strip()
        email = request.POST.get("email").strip()
        subject = request.POST.get("subject").strip()
        message = request.POST.get("message").strip()

        name_regex = r'^[A-Za-z\s]{2,50}$'
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

        if not re.match(name_regex, name):
            messages.error(request, "Name must contain only letters.")

        elif not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")

        elif len(subject) < 3:
            messages.error(request, "Subject must be at least 3 characters.")

        elif len(message) < 10:
            messages.error(request, "Message must be at least 10 characters.")

        else:

            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            messages.success(request, "Your message has been sent!")

            print("Message saved!")

    return render(request, "core/contact.html")



def subscribe(request):
    if request.method == "POST":

        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get("email")

        if email:
            obj, created = Subscriber.objects.get_or_create(email=email)

            if created:
                messages.success(request, "Subscribed successfully!")
            else:
                messages.warning(request, "You are already subscribed!")

    return redirect(request.META.get('HTTP_REFERER', '/'))