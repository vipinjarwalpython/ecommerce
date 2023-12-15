from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from seller.models import Seller, Product
from .models import SellerWallet
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from seller.models import Category

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

        return redirect("/seller/login/")
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
            return redirect("/seller/product/")

    return render(request, "seller_login.html")


def seller_logout(request):
    logout(request)
    return redirect("/")


def dashboard(request):
    return render(request, "sellerdashboard.html")


def product_registration(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get or create the Seller instance for the logged-in user
        user = request.user
        seller_instance, created = Seller.objects.get_or_create(seller=user)

        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            price = request.POST.get("price")
            image = request.FILES.get("image")

            # Create a Product instance associated with the Seller
            product = Product.objects.create(
                seller=seller_instance,
                name=name,
                description=description,
                price=price,
                image=image,
                approved=False,
            )
            print(product.approved)
            # Check for admin approval or custom approval process
    userid = request.user
    print(userid)
    seller = Seller.objects.get(seller=userid)
    print(seller)

    products = Product.objects.filter(seller=seller)
    return render(request, "product_registration.html", {"products": products})


# def product_registration(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         description = request.POST.get("description")
#         price = request.POST.get("price")
#         image = request.FILES.get("image")
#         product = Product.objects.create(
#             name=name, description=description, price=price, image=image
#         )
#         product.save()
#         return redirect("/seller/product/")

#     products = Product.objects.all()
#     return render(request, "product_registration.html", {"products": products})


def update_product(request, id):
    product = Product.objects.get(pk=id)
    return render(request, "update_product.html", {"product": product})


def do_update_product(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        categoryid = request.POST.get("category")
    product = Product.objects.get(pk=id)

    if image:
        product.image = image
        product.save()
        return redirect("/seller/product/")
    product.name = name
    product.description = description
    product.price = price
    new_category = Category.objects.get(id=categoryid)
    product.category = new_category
    product.save()
    return redirect("/seller/product/")


def delete_product(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return redirect("/seller/product/")


def product_list(request):
    products = Product.objects.filter(approved=True)

    return render(request, "shop.html", {"products": products})


def seller_wallet(request):
    try:
        seller_wallet = SellerWallet.objects.get(user=request.user)
    except SellerWallet.DoesNotExist:
        # Redirect the user to create the wallet if it doesn't exist
        return redirect("/seller/create_seller_wallet/")

    return render(request, "seller_wallet.html", {"seller_wallet": seller_wallet})


@login_required
def add_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            try:
                seller_wallet = SellerWallet.objects.get(user=request.user)

            except SellerWallet.DoesNotExist:
                # Redirect the user to create the wallet if it doesn't exist
                return redirect("/seller/create_seller_wallet/")

            seller_wallet.balance += amount
            seller_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/seller/seller_wallet/")

    return render(request, "add_funds.html")


def create_seller_wallet(request):
    if SellerWallet.objects.filter(user=request.user).exists():
        return redirect("add_funds")

    SellerWallet.objects.create(user=request.user, balance=0)

    return redirect("add_funds")
