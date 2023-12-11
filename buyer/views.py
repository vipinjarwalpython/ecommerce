from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer

# Create your views here.


def buyer_signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        print(password1, password2)

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/buyer_signup/")

        if not User.objects.filter(username=username).exists():
            buyer = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password1,
            )

            buyer_extra_fields = Buyer.objects.create(
                buyer=buyer,
                phone=phone,
            )

            return redirect("/buyer/login/")

        else:
            messages.error(request, "Username already exists")
            return redirect("/buyer/signup/")
    return render(request, "buyer_signup.html")


def buyer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username is not found")
            return redirect("/buyer/login/")

        buyer = authenticate(username=username, password=password)
        print(buyer)

        if buyer is None:
            messages.error(request, "password is incorrect")
            return redirect("/buyer/login/")
        else:
            login(request, buyer)
            return redirect("/")
    return render(request, "buyer_login.html")


def buyer_logout(request):
    logout(request)
    return redirect("/")
