from django.shortcuts import render, redirect
from buyer.models import Buyer
from seller.models import Seller
from seller.models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


from django.shortcuts import render

# Create your views here.
