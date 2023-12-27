from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer, CartItem, BuyersBilling, BillItems, BillClone
from seller.models import Product, Seller
from superadmin.models import Wallet
from decimal import Decimal
from django.contrib.auth.decorators import login_required

# Create your views here.


def buyer_signup(request):
    try:
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
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "buyer_signup.html")


def buyer_login(request):
    try:
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
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "buyer_login.html")


@login_required(login_url="/buyer/login/")
def buyer_logout(request):
    try:
        logout(request)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect("/")

    # product add and purchase
    # def product_list(request):
    try:
        products = Product.objects.all()
        return render(request, "shop.html", {"products": products})

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def view_cart(request):
    try:
        total_price = []
        user = request.user
        if not user.is_authenticated:
            return redirect("/")
        else:
            cart_items = CartItem.objects.filter(user=request.user)

            for item in cart_items:
                item.total_price = item.product.price * item.quantity
                item.save()

                total_price.append(item.total_price)

                if item.quantity == 0:
                    cart_items.delete()

            total__product_price = sum(total_price)

            return render(
                request,
                "cart.html",
                {
                    "cart_items": cart_items,
                    "total__product_price": total__product_price,
                },
            )

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def add_to_cart(request, id):
    try:
        product = Product.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user
        )

        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        return redirect("/shop/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def remove_from_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
        return redirect("/cart/")

    except CartItem.DoesNotExist:
        messages.error(request, "Cart item not found.")
        return redirect("/cart/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/cart/")


@login_required(login_url="/buyer/login/")
def plus_to_cart(request, id):
    try:
        product = Product.objects.get(id=id)
        print(product.quantity)
        if product.quantity > 0:
            cart_item, created = CartItem.objects.get_or_create(
                product=product, user=request.user
            )
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
            product = Product.objects.get(id=cart_item.product.id)
            product.quantity = product.quantity - 1
            product.save()
            return redirect("/cart/")
        else:
            messages.error(request, "Product Quantity is less than 0")
            return redirect("/cart/")

    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("/cart/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/cart/")


@login_required(login_url="/buyer/login/")
def minus_from_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        if cart_item.quantity > 0:
            cart_item.quantity = cart_item.quantity - 1
            cart_item.save()
            product = Product.objects.get(id=cart_item.product.id)
            product.quantity = product.quantity + 1
            product.save()
            return redirect("/cart/")
        else:
            messages.error(request, "Cart item quantity is already 0")
            return redirect("/cart/")

    except CartItem.DoesNotExist:
        messages.error(request, "Cart item not found.")
        return redirect("/cart/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/cart/")


@login_required(login_url="/buyer/login/")
def billing(request):
    try:
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

        buy_wallet = Wallet.objects.get(walletuser=request.user)
        if buy_wallet.balance <= 0:
            messages.error(
                request, "Your wallet is empty! Please add funds to your wallet."
            )
            # return redirect("/bill/")

        total_price = []
        for item in cart_item:
            item.total_price = item.product.price * item.quantity
            item.save()

            total_price.append(item.total_price)

        total__product_price = sum(total_price)
        return render(
            request,
            "checkout.html",
            {
                "cart_item": cart_item,
                "total_ammount": total__product_price,
                "buy_wallet": buy_wallet,
            },
        )

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def bill_confirm(request):
    try:
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

        buy_wallet = Wallet.objects.get(walletuser=request.user)
        if buy_wallet.balance < total__product_price:
            messages.error(
                request,
                "Your wallet ammount is less than the total amount. Please add funds to your wallet.",
            )
            return render(
                request,
                "bill_confirmation.html",
                {
                    "cart_item": cart_item,
                    "cust_bill": last_bill,
                    "total_ammount": total__product_price,
                    "buy_wallet": buy_wallet,
                },
            )

        return render(
            request,
            "bill_confirmation.html",
            {
                "cart_item": cart_item,
                "cust_bill": last_bill,
                "total_ammount": total__product_price,
                "buy_wallet": buy_wallet,
            },
        )

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def thankyou(request):
    try:
        total_ammount = 0
        userid = request.user
        cart_item = CartItem.objects.filter(user_id=userid)

        for item in cart_item:
            final_bill = BillItems.objects.create(
                product=item.product,
                quantity=item.quantity,
                user=item.user,
                total_price=item.total_price,
            )
            final_bill.save()

            total_ammount += item.product.price

            product = Product.objects.get(name=item.product)
            print(product.quantity)
            if product.quantity > 0:
                product.quantity = product.quantity - item.quantity
                product.save()
            else:
                messages.error(request, "Product Quanity is less than 0")

            billclone = BillClone.objects.create(bill_item=final_bill)
            billclone.save()

        buy_wallet = Wallet.objects.get(walletuser=request.user)
        if buy_wallet.balance == 0:
            messages.error(request, "Your wallet has no balance.")
        remain_ammount = buy_wallet.balance - total_ammount

        buy_wallet.balance = remain_ammount
        buy_wallet.save()

        cart_item.delete()
        return render(request, "thankyou.html")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def add_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)
                buyer_wallet = Wallet.objects.get(walletuser=request.user)

                buyer_wallet.balance += amount
                buyer_wallet.save()
                # Add transaction history and other logic as needed
                return redirect("/buyer/wallet/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "add_funds.html")


@login_required(login_url="/buyer/login/")
def withdraw_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)
                buyer_wallet = Wallet.objects.get(walletuser=request.user)
                if buyer_wallet.balance == 0:
                    messages.error(request, "Your wallet has no balance.")

                buyer_wallet.balance -= amount
                buyer_wallet.save()
                # Add transaction history and other logic as needed
                return redirect("/buyer/wallet/")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "Withdraw_funds.html")


@login_required(login_url="/buyer/login/")
def buyer_wallet(request):
    try:
        buy_wallet = Wallet.objects.get(walletuser=request.user)
        return render(request, "buyer_wallet.html", {"buy_wallet": buy_wallet})

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")


@login_required(login_url="/buyer/login/")
def buyer_dashboard(request):
    try:
        userid = request.user.id
        items = BillItems.objects.filter(user=userid)
        return render(request, "buyer_dashboard.html", {"items": items})

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/")
