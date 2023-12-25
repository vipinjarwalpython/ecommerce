from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer, CartItem, BuyersBilling, BillItems
from seller.models import Product, Seller
from superadmin.models import Wallet
from decimal import Decimal

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

            Buyer.objects.create(
                buyer=buyer,
                phone=phone,
            )

            Wallet.objects.create(walletuser=buyer, balance=0, user_type="buyer")
            buyer.save()
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

        buyer_user = User.objects.get(username=username)

        if not Buyer.objects.filter(buyer_id=buyer_user.id).exists():
            messages.error(request, "Username is not found")
            return redirect("/buyer/login/")

        buyer = authenticate(request, username=username, password=password)

        if buyer is None:
            messages.error(request, "Password is Incorrect")
            return redirect("/buyer/login/")
        else:
            login(request, buyer)
            return redirect("/")
    return render(request, "buyer_login.html")


def buyer_logout(request):
    logout(request)
    return redirect("/")


# product add and purchase
def product_list(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})


def view_cart(request):
    total_price = []
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.save()

        total_price.append(item.total_price)

    total__product_price = sum(total_price)

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total__product_price": total__product_price,
        },
    )


def add_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=request.user
    )
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=request.user
    )
    cart_item.quantity = cart_item.quantity + 1
    cart_item.save()
    return redirect("/shop/")


def remove_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect("/cart/")


def plus_to_cart(request, id):
    product = Product.objects.get(id=id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product, user=request.user
    )
    cart_item.quantity = cart_item.quantity + 1
    cart_item.save()
    return redirect("/cart/")


def minus_from_cart(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.quantity = cart_item.quantity - 1
    cart_item.save()
    return redirect("/cart/")


def billing(request):
    userid = request.user.id
    cart_item = CartItem.objects.filter(user_id=userid)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        city = request.POST.get("city")
        postal = request.POST.get("postal")
        country = request.POST.get("country")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        notes = request.POST.get("notes")

        cust_bill = BuyersBilling.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            city=city,
            postal=postal,
            country=country,
            email=email,
            phone=phone,
            notes=notes,
        )
        cust_bill.save()
        return redirect("/bill-confirmation/")

    total_price = []
    for item in cart_item:
        item.total_price = item.product.price * item.quantity
        item.save()

        total_price.append(item.total_price)

    total__product_price = sum(total_price)
    return render(
        request,
        "checkout.html",
        {"cart_item": cart_item, "total_ammount": total__product_price},
    )


def bill_confirm(request):
    userid = request.user
    cart_item = CartItem.objects.filter(user_id=userid)
    # print(cart_item)
    cust_bill = BuyersBilling.objects.filter(user=userid)
    last_bill = cust_bill[len(cust_bill) - 1]

    total_price = []
    for item in cart_item:
        item.total_price = item.product.price * item.quantity
        item.save()

        total_price.append(item.total_price)

    total__product_price = sum(total_price)

    return render(
        request,
        "bill_confirmation.html",
        {
            "cart_item": cart_item,
            "cust_bill": last_bill,
            "total_ammount": total__product_price,
        },
    )


def thankyou(request):
    total_ammount = 0
    userid = request.user
    cart_item = CartItem.objects.filter(user_id=userid)

    for item in cart_item:
        final_bill = BillItems.objects.create(
            # buyer_details =
            product=item.product,
            quantity=item.quantity,
            user=item.user,
            total_price=item.total_price,
        )
        final_bill.save()

        total_ammount += item.product.price

        product = Product.objects.get(name=item.product)
        print(product.quantity)
        product.quantity = product.quantity - item.quantity
        product.save()

    buy_wallet = Wallet.objects.get(walletuser=request.user)
    remain_ammount = buy_wallet.balance - total_ammount

    buy_wallet.balance = remain_ammount
    buy_wallet.save()

    user_item = CartItem.objects.all()

    for u in user_item:
        # Send Money buyer wallet to seller wallet deducted 95% of total bill with indivual product price
        sellerwallet = Wallet.objects.get(walletuser_id=u.product.seller.seller.id)
        sellerwallet.balance = Decimal(sellerwallet.balance) + Decimal(
            (u.total_price * 95) / 100
        )
        sellerwallet.save()
        # Send Money buyer wallet to superadmin wallet 5% of total bill with indivual product price
        superwallet = Wallet.objects.get(user_type="superadmin")
        superwallet.balance = Decimal(superwallet.balance) + Decimal(
            (u.total_price * 5) / 100
        )
        superwallet.save()

    cart_item.delete()
    return render(request, "thankyou.html")


def add_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            buyer_wallet = Wallet.objects.get(walletuser=request.user)

            buyer_wallet.balance += amount
            buyer_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/buyer/wallet/")

    return render(request, "add_funds.html")


def withdraw_funds(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is not None:
            amount = Decimal(amount)
            buyer_wallet = Wallet.objects.get(walletuser=request.user)

            buyer_wallet.balance -= amount
            buyer_wallet.save()
            # Add transaction history and other logic as needed
            return redirect("/buyer/wallet/")

    return render(request, "Withdraw_funds.html")


def buyer_wallet(request):
    buy_wallet = Wallet.objects.get(walletuser=request.user)

    return render(request, "buyer_wallet.html", {"buy_wallet": buy_wallet})


def buyer_dashboard(request):
    userid = request.user.id
    items = BillItems.objects.filter(user=userid)

    return render(request, "buyer_dashboard.html", {"items": items})
