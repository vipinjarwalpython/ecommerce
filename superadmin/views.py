from django.shortcuts import render, redirect
from buyer.models import Buyer
from seller.models import Seller
from seller.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math
from .models import Wallet
from decimal import Decimal
from seller.models import Category

# from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/")
def superadmin_dashboard(request):
    if request.method == "POST":
        id = request.POST.get("id")
        product = Product.objects.get(id=id)
        print(product.id)
        if product.approved:
            product.approved = False
            product.save()
        else:
            product.approved = True
            product.save()
        return redirect("/superadmin/dashboard/")

    buyers = Buyer.objects.all()
    seller = Seller.objects.all()
    product = Product.objects.all()

    # print(buyers)
    # print(seller)
    # print(product)

    return render(
        request,
        "superadmin_dashboard.html",
        {"buyers": buyers, "seller": seller, "product": product},
    )


def superadmin_login(request):
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("password")
        if username == "superadmin" and password == "super12345":
            user = authenticate(username="superadmin", password="super12345")

            if user is None:
                messages.error(request, "Invalid username or password")
                print(messages)
                return redirect("/")
            else:
                login(request, user)
                messages.success(request, "Login successful")
                return redirect("/superadmin/dashboard/")

    return render(request, "superadminlogin.html")


def superadmin_logout(request):
    logout(request)
    return redirect("/")


def seller_list(request):
    seller = Seller.objects.all()

    return render(request, "seller_list.html", {"seller": seller})


def product_list(request):
    product = Product.objects.all()

    return render(request, "product_list.html", {"product": product})


def sellerwise_list(request):
    seller = Seller.objects.all()
    return render(request, "sellerwiselist.html", {"seller": seller})


def sellerwiseindividuallist(request, id):
    seller = Seller.objects.get(pk=id)

    product = Product.objects.filter(seller=seller)
    print("############################################")
    print(product)
    return render(request, "sellerwiselist_select.html", {"product": product})


def categorywise_productlist(request):
    category = Category.objects.all()
    # print(category)
    return render(request, "categorywise_productlist.html", {"category": category})


def product_categorywise(request, id):
    category = Category.objects.get(id=id)
    product = Product.objects.filter(category=category)
    print(product)
    return render(request, "category_product.html", {"product": product})


def superadmin_add_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            try:
                superadmin_wallet = Wallet.objects.get(walletuser=request.user)

            except Wallet.DoesNotExist:
                # Redirect the user to create the wallet if it doesn't exist
                return redirect("/")

            superadmin_wallet.balance += amount
            superadmin_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/superadmin/superadmin_wallet/")

    return render(request, "superadmin_add_funds.html")


def superadmin_wallet(request):
    superadmin_wallet = Wallet.objects.get(walletuser=request.user)

    return render(
        request, "superadmin_wallet.html", {"superadmin_wallet": superadmin_wallet}
    )


def walletwise_sellerlist(request):
    seller = Seller.objects.all()
    wallet = Wallet.objects.all()

    return render(
        request, "walletwise_sellerlist.html", {"seller": seller, "wallet": wallet}
    )
