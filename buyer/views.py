from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer, CartItem, BuyersBilling, BillItems, BillClone
from seller.models import Product, Seller
from superadmin.models import Wallet
from decimal import Decimal


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
        # Log the exception or handle it as needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/buyer/signup/")

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
        # Log the exception or handle it as needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/buyer/login/")

    return render(request, "buyer_login.html")


def buyer_logout(request):
    try:
        logout(request)
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during logout: {str(e)}")

    return redirect("/")


# product add and purchase
def product_list(request):
    try:
        products = Product.objects.all()
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving products: {str(e)}")
        products = []

    return render(request, "shop.html", {"products": products})


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
        # Log the exception or handle it as needed
        print(f"An error occurred while viewing the cart: {str(e)}")
        return redirect("/")


def add_to_cart(request, id):
    try:
        product = Product.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user
        )
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        return redirect("/shop/")

    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        print(f"Product with id {id} does not exist.")
        return redirect("/shop/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while adding to the cart: {str(e)}")
        return redirect("/shop/")


def remove_from_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        cart_item.delete()
        return redirect("/cart/")

    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        print(f"Cart item with id {id} does not exist.")
        return redirect("/cart/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while removing from the cart: {str(e)}")
        return redirect("/cart/")


def plus_to_cart(request, id):
    try:
        product = Product.objects.get(id=id)
        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user
        )
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        return redirect("/cart/")

    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        print(f"Product with id {id} does not exist.")
        return redirect("/cart/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while adding to the cart: {str(e)}")
        return redirect("/cart/")


def minus_from_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id)
        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()
        return redirect("/cart/")

    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        print(f"Cart item with id {id} does not exist.")
        return redirect("/cart/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while subtracting from the cart: {str(e)}")
        return redirect("/cart/")


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

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during billing: {str(e)}")
        return redirect("/checkout-error/")


def bill_confirm(request):
    try:
        userid = request.user
        cart_item = CartItem.objects.filter(user_id=userid)

        # Assuming BuyersBilling has a ForeignKey field 'cart_item' linking it to CartItem
        cust_bill = BuyersBilling.objects.filter(user=userid, cart_item__in=cart_item)
        last_bill = cust_bill.last()

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

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during bill confirmation: {str(e)}")
        return redirect("/bill-confirm-error/")


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
            product.quantity = product.quantity - item.quantity
            product.save()

            billclone = BillClone.objects.create(bill_item=final_bill)
            billclone.save()

        buy_wallet = Wallet.objects.get(walletuser=request.user)
        remain_ammount = buy_wallet.balance - total_ammount

        buy_wallet.balance = remain_ammount
        buy_wallet.save()

        cart_item.delete()
        return render(request, "thankyou.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during the 'thank you' process: {str(e)}")
        return redirect("/thankyou-error/")


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

        return render(request, "add_funds.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during fund addition: {str(e)}")
        return redirect("/add-funds-error/")


def withdraw_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)
                buyer_wallet = Wallet.objects.get(walletuser=request.user)

                if amount <= buyer_wallet.balance:
                    buyer_wallet.balance -= amount
                    buyer_wallet.save()
                    # Add transaction history and other logic as needed
                    return redirect("/buyer/wallet/")
                else:
                    # Handle insufficient funds
                    return redirect("/withdraw-funds-error/")

        return render(request, "withdraw_funds.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during fund withdrawal: {str(e)}")
        return redirect("/withdraw-funds-error/")


def buyer_wallet(request):
    try:
        buy_wallet = Wallet.objects.get(walletuser=request.user)
        return render(request, "buyer_wallet.html", {"buy_wallet": buy_wallet})

    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist for the user
        print(f"Wallet not found for user {request.user}.")
        return render(request, "wallet_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while accessing the wallet: {str(e)}")
        return redirect("/wallet-error/")


def buyer_dashboard(request):
    try:
        userid = request.user.id
        items = BillItems.objects.filter(user=userid)
        return render(request, "buyer_dashboard.html", {"items": items})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while accessing the buyer dashboard: {str(e)}")
        return redirect("/buyer-dashboard-error/")
