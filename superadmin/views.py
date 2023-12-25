from django.shortcuts import render, redirect
from buyer.models import Buyer, BillClone
from seller.models import Seller
from seller.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math
from .models import Wallet
from decimal import Decimal
from seller.models import Category
from buyer.models import CartItem
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
    category = Category.objects.all()

    # print(buyers)
    # print(seller)
    # print(product)

    return render(
        request,
        "superadmin_dashboard.html",
        {"buyers": buyers, "seller": seller, "product": product, "category": category},
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


def buyer_list(request):
    buyer = Buyer.objects.all()

    return render(request, "buyer_list.html", {"buyer": buyer})


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


def superadmin_withdraw_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            try:
                superadmin_wallet = Wallet.objects.get(walletuser=request.user)

            except Wallet.DoesNotExist:
                # Redirect the user to create the wallet if it doesn't exist
                return redirect("/")

            superadmin_wallet.balance = superadmin_wallet.balance - amount
            superadmin_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/superadmin/superadmin_wallet/")

    return render(request, "superadmin_withdraw_funds.html")


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


def settlement(request):
    # billclone = BillClone.objects.filter(bill_item_id=user.id)
    billclone = BillClone.objects.all()

    return render(request, "settlement.html", {"billclone": billclone})


def final_settlement(request, id):
    billclone = BillClone.objects.get(id=id)
    # print(billclone.bill_item.total_price)

    # Send Money buyer wallet to seller wallet deducted 95% of total bill with indivual product price
    sellerwallet = Wallet.objects.get(
        walletuser_id=billclone.bill_item.product.seller.seller.id
    )
    # print(sellerwallet)
    sellerwallet.balance = Decimal(sellerwallet.balance) + Decimal(
        (billclone.bill_item.total_price * 95) / 100
    )
    sellerwallet.save()

    # Send Money buyer wallet to superadmin wallet 5% of total bill with indivual product price
    superwallet = Wallet.objects.get(user_type="superadmin")
    print(superwallet)
    superwallet.balance = Decimal(superwallet.balance) + Decimal(
        (billclone.bill_item.total_price * 5) / 100
    )
    superwallet.save()

    billclone.delete()

    return render(request, "final-settlement.html")
