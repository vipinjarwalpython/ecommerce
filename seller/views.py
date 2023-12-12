from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from seller.models import Seller, Product

# Create your views here.


def seller_register(request):
    if request.method == "POST":
        seller_firstname = request.POST.get("seller_firstname")
        seller_lastname = request.POST.get("seller_lastname")
        seller_email = request.POST.get("seller_email")
        seller_mobilenumber = request.POST.get("seller_mobilenumber")
        seller_username = request.POST.get("seller_username")
        seller_password1 = request.POST.get("seller_password1")
        seller_password2 = request.POST.get("seller_password2")
        print(seller_password1)
        print(seller_password2)
        user = User.objects.create_user(
            first_name=seller_firstname,
            last_name=seller_lastname,
            email=seller_email,
            username=seller_username,
            password=seller_password1,
        )

        seller = Seller.objects.create(
            seller=user,
            seller_mobilenumber=seller_mobilenumber,
        )

        return redirect("/seller_login/")
    return render(request, "seller_register.html")


def seller_login(request):
    if request.method == "POST":
        seller_username = request.POST.get("seller_username")
        seller_password = request.POST.get("seller_password")

        user = authenticate(username=seller_username, password=seller_password)

        print(user)
        if user is None:
            messages.error(request, "Invalid username or password")

        else:
            login(request, user)
            return redirect("/")

    return render(request, "seller_login.html")


def seller_logout(request):
    logout(request)
    return redirect("/")


def dashboard(request):
    return render(request, "sellerdashboard.html")


def product_registration(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        product = Product.objects.create(
            name=name, description=description, price=price, image=image
        )
        product.save()
        return redirect("/seller/product/")

    products = Product.objects.all()
    return render(request, "product_registration.html", {"products": products})


def product_list(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})
