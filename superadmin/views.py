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
from buyer.models import BillItems
from django.contrib.auth.models import User

# from django.contrib.auth.decorators import login_required

# Create your views here.


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
        print(username)
        print(password)
        if username == "superadmin" and password == "super12345":
            user = authenticate(username="superadmin", password="super12345")
            print(user)

            if user is not None:
                login(request, user)
                return redirect("/superadmin/dashboard/")

            else:
                messages.error(request, "Invalid username or password")
                return redirect("/")

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
    wallet = Wallet.objects.filter(user_type="seller")

    return render(
        request, "walletwise_sellerlist.html", {"seller": seller, "wallet": wallet}
    )


# def settlement(request):
    user_item_list = []
    user_price_list = []

    # items_purchased = BillItems.objects.all()
    users = User.objects.all()
    for user in users:
        user_item = BillItems.objects.filter(user_id=user.id)
        for u in user_item:
            user_item_list.append(u.user)
            user_price_list.append(u.total_price)
    #         user_item_list.append(u.total_price)
    print(user_item_list)
    print(user_price_list)

    return render(
        request,
        "settlement.html",
    )
    # total_price = 0
    # for items in items_purchased:
    #     # print(items.user)
    #     print(items)
    # print("===================================================")
    # raw_amount = items.product.price * items.quantity
    # total_price = total_price + raw_amount
    # print("===================================================")
    # print(total_price)

    #     if items.user == "vicky":
    #         total_price += items.product.price
    # print(total_price)

    return render(request, "settlement.html")
