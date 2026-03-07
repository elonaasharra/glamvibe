from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
import uuid
from .models import EmailVerification
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        # nuk lejon login nese fushat jane bosh
        if not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("login")

        #kontrollon nese ekziston user me ate email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        #kontrollon nese username dhe pass perkojne me te dhenat qe jan rregjistruar ne db gjat rregjistrimit

        if user is not None:

            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:

                if authenticated_user.is_active: #useri mund te hyje vetem nese ka verifikuar emailin
                    login(request, authenticated_user)
                    return redirect("home")

                else:
                    messages.error(request, "Please verify your email first.")

            else:
                messages.error(request, "Invalid email or password.")

        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'accounts/login.html')


def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # validation
        if not username or not email or not password or not password2:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/register.html", {
                "username": username,
                "email": email
            })

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/register.html", {
                "username": username,
                "email": email
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "accounts/register.html", {
                "username": username,
                "email": email
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "accounts/register.html", {
                "username": username,
                "email": email
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False
        user.save()

        token = str(uuid.uuid4())

        EmailVerification.objects.create(
            user=user,
            token=token
        )

        verification_link = f"http://127.0.0.1:8000/accounts/verify/{token}/"

        send_mail(
            "Verify your email",
            f"Click the link to verify your account: {verification_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Account created! Please check your email to verify your account.")
        return redirect("login")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect('home')


def verify_email(request, token):

    try:
        verification = EmailVerification.objects.get(token=token)
    except EmailVerification.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect("login")

    user = verification.user
    user.is_active = True
    user.save()

    verification.delete()

    messages.success(request, "Email verified successfully.")

    return redirect("login")