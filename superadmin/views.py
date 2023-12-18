from django.shortcuts import render, redirect
from buyer.models import Buyer
from seller.models import Seller
from seller.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SuperAdminWallet
from decimal import Decimal

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


def categorywise_productlist(request):
    return render(request, "categorywise_productlist.html")


def sellerwise_list(request):
    seller = Seller.objects.all()
    return render(request, "sellerwiselist.html", {"seller": seller})


def sellerwiseindividuallist(request, id):
    seller = Seller.objects.get(pk=id)

    product = Product.objects.filter(seller=seller)
    print("############################################")
    print(product)
    return render(request, "sellerwiselist_select.html", {"product": product})


def Electronicsandmobile(request):
    product = Product.objects.all()
    return render(request, "Electronicsandmobile.html", {"product": product})


def Fashionandlifestyle(request):
    product = Product.objects.all()
    return render(request, "Fashionandlifestyle.html", {"product": product})


def Media(request):
    product = Product.objects.all()
    return render(request, "Media.html", {"product": product})


def Homeandappliances(request):
    product = Product.objects.all()
    return render(request, "Homeandappliances.html", {"product": product})


def Homemadeandcraftings(request):
    product = Product.objects.all()
    return render(request, "Homemadeandcraftings.html", {"product": product})


def Footwear(request):
    product = Product.objects.all()
    return render(request, "Footwear.html", {"product": product})


def Giftsandhampers(request):
    product = Product.objects.all()
    return render(request, "Giftsandhampers.html", {"product": product})


def Festivalshoppingitems(request):
    product = Product.objects.all()
    return render(request, "Festivalshoppingitems.html", {"product": product})


def test(request):
    return render(request, "test.html")


def seller_wallet(request):
    try:
        superadmin_wallet = SuperAdminWallet.objects.get(user=request.user)
    except SuperAdminWallet.DoesNotExist:
        # Redirect the user to create the wallet if it doesn't exist
        return redirect("/superadmin/createsuperadminwallet/")

    return render(
        request, "superadmin_wallet.html", {"superadmin_wallet": superadmin_wallet}
    )


@login_required
def add_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            try:
                superadmin_wallet = SuperAdminWallet.objects.get(user=request.user)

            except superadmin_wallet.DoesNotExist:
                # Redirect the user to create the wallet if it doesn't exist
                return redirect("/seller/create_seller_wallet/")

            superadmin_wallet.balance += amount
            superadmin_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/superadmin/superadmin_wallet/")

    return render(request, "add_funds_superadmin.html")


def create_superadmin_wallet(request):
    if SuperAdminWallet.objects.filter(user=request.user).exists():
        return redirect("add_funds")

    SuperAdminWallet.objects.create(user=request.user, balance=0)

    return redirect("/superadmin/add_funds_superadmin/")


