from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer, CartItem, BuyersBilling, BillItems, BillClone
from seller.models import Product, Seller
from superadmin.models import Wallet
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render, redirect


# Create your views here.


def buyer_signup(request):
    if request.method == "POST":
        try:
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
            # Handle the exception, you can print the error for debugging
            print(f"An error occurred: {e}")
            messages.error(
                request, "An error occurred during signup. Please try again."
            )
            return redirect("/buyer/signup/")

    return render(request, "buyer_signup.html")


def buyer_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            buyer = Buyer.objects.get(buyer_id=user.id)

            # If both user and buyer are found, attempt authentication
            buyer_user = authenticate(request, username=username, password=password)

            if buyer_user is not None:
                login(request, buyer_user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
                return redirect("/buyer/login/")

        except User.DoesNotExist:
            messages.error(request, "Username is not found")
            return redirect("/buyer/login/")

        except Buyer.DoesNotExist:
            messages.error(request, "Username is not found")
            return redirect("/buyer/login/")

        except Exception as e:
            # Handle other exceptions, log the error, and display a generic message
            print(f"An error occurred: {e}")
            messages.error(request, "An error occurred during login. Please try again.")
            return redirect("/buyer/login/")

    return render(request, "buyer_login.html")


def buyer_logout(request):
    try:
        logout(request)
    except Exception as e:
        # Handle exceptions that might occur during logout
        print(f"An error occurred during logout: {e}")

    return redirect("/")


# product add and purchase
def product_list(request):
    products = Product.objects.all()

    # Pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page = request.GET.get("page")

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, "shop.html", {"products": products})


def view_cart(request):
    try:
        total_price = 0
        user = request.user

        if not user.is_authenticated:
            raise ValueError("User is not authenticated")

        cart_items = CartItem.objects.filter(user=user)

        items_to_delete = []

        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            total_price += item.total_price

            if item.quantity == 0:
                items_to_delete.append(item)

        # Delete items with quantity 0 outside the loop
        for item in items_to_delete:
            item.delete()

        return render(
            request,
            "cart.html",
            {
                "cart_items": cart_items,
                "total_product_price": total_price,
            },
        )

    except ValueError as ve:
        # Handle the specific exception for unauthenticated users
        print(f"Error: {ve}")
        return redirect("/")

    except Exception as e:
        # Handle other exceptions, log the error, and display a generic message
        print(f"An error occurred during cart view: {e}")
        return render(
            request,
            "error_page.html",
            {"error_message": "An error occurred. Please try again."},
        )


def add_to_cart(request, id):
    try:
        product = get_object_or_404(Product, id=id)

        if not request.user.is_authenticated:
            # Redirect or handle non-authenticated users as needed
            return redirect("/login/")  # Adjust the URL based on your actual login page

        cart_item, created = CartItem.objects.get_or_create(
            product=product, user=request.user
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Provide feedback to the user that the item has been added to the cart
        messages.success(request, "Product added to the cart successfully.")

        return redirect("/shop/")  # Adjust the URL based on your actual shop page

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred during add_to_cart: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect("/shop/")  # Redirect to shop page or another appropriate page


def remove_from_cart(request, id):
    try:
        cart_item = get_object_or_404(CartItem, id=id)
        cart_item.delete()

        # Provide feedback to the user that the item has been removed from the cart
        messages.success(request, "Product removed from the cart successfully.")

    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        messages.warning(request, "This item does not exist in your cart.")

    except Exception as e:
        # Handle other exceptions, log the error, and display a generic message
        print(f"An error occurred during remove_from_cart: {e}")
        messages.error(request, "An error occurred. Please try again.")

    return redirect("/cart/")  # Adjust the URL based on your actual cart page


def plus_to_cart(request, id):
    try:
        product = get_object_or_404(Product, id=id)

        if not request.user.is_authenticated:
            # Redirect or handle non-authenticated users as needed
            return redirect("/login/")  # Adjust the URL based on your actual login page

        if product.quantity > 0:
            cart_item, created = CartItem.objects.get_or_create(
                product=product, user=request.user
            )
            cart_item.quantity += 1
            cart_item.save()

            product.quantity -= 1
            product.save()

            # Provide feedback to the user that the item quantity has been increased
            messages.success(request, "Product quantity increased successfully.")
        else:
            messages.warning(request, "Product quantity is less than or equal to 0.")

    except Product.DoesNotExist:
        # Handle the case where the product does not exist
        messages.error(request, "This product does not exist.")

    except Exception as e:
        # Handle other exceptions, log the error, and display a generic message
        print(f"An error occurred during plus_to_cart: {e}")
        messages.error(request, "An error occurred. Please try again.")

    return redirect("/cart/")  # Adjust the URL based on your actual cart page


def minus_from_cart(request, id):
    try:
        cart_item = get_object_or_404(CartItem, id=id)

        if not request.user.is_authenticated:
            # Redirect or handle non-authenticated users as needed
            return redirect("/login/")  # Adjust the URL based on your actual login page

        if cart_item.quantity > 0:
            cart_item.quantity -= 1
            cart_item.save()

            product = Product.objects.get(id=cart_item.product.id)
            product.quantity += 1
            product.save()

            # Provide feedback to the user that the item quantity has been decreased
            messages.success(request, "Product quantity decreased successfully.")
        else:
            messages.warning(request, "Product quantity is already 0.")

    except CartItem.DoesNotExist:
        # Handle the case where the cart item does not exist
        messages.error(request, "This cart item does not exist.")

    except Exception as e:
        # Handle other exceptions, log the error, and display a generic message
        print(f"An error occurred during minus_from_cart: {e}")
        messages.error(request, "An error occurred. Please try again.")

    return redirect("/cart/")  # Adjust the URL based on your actual cart page


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    CartItem,
    BuyersBilling,
    Wallet,
)  # Adjust the import based on your actual model location


def billing(request):
    try:
        if not request.user.is_authenticated:
            return redirect(
                "/login/"
            )  # Redirect non-authenticated users to the login page

        userid = request.user.id
        cart_items = CartItem.objects.filter(user_id=userid)

        if request.method == "POST":
            # Use Django forms for handling form validation and data cleaning

            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            address = request.POST.get("address")
            city = request.POST.get("city")
            postal = request.POST.get("postal")
            country = request.POST.get("country")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            notes = request.POST.get("notes")

            # Create a billing entry
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

            # Update wallet balance
            buy_wallet = Wallet.objects.get(walletuser=request.user)
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            if buy_wallet.balance < total_price:
                messages.error(request, "Insufficient funds in your wallet.")
                return redirect("/bill/")

            buy_wallet.balance -= total_price
            buy_wallet.save()

            # Clear the cart items
            cart_items.delete()

            messages.success(request, "Billing successful. Thank you!")

            return redirect("/bill-confirmation/")

        buy_wallet = Wallet.objects.get(walletuser=request.user)

        if buy_wallet.balance <= 0:
            messages.error(
                request, "Your wallet is empty! Please add funds to your wallet."
            )

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return render(
            request,
            "checkout.html",
            {
                "cart_items": cart_items,
                "total_amount": total_price,
                "buy_wallet": buy_wallet,
            },
        )

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred during billing: {e}")
        messages.error(request, "An error occurred during billing. Please try again.")
        return redirect("/bill/")


def bill_confirm(request):
    try:
        userid = request.user
        cart_item = CartItem.objects.filter(user_id=userid)

        # Check if there are any cart items
        if not cart_item.exists():
            messages.warning(request, "No items in the cart.")
            return redirect(
                "/cart/"
            )  # Redirect to cart page or another appropriate page

        cust_bill = BuyersBilling.objects.filter(user=userid)

        # Check if there are any billing entries
        if not cust_bill.exists():
            messages.warning(request, "No billing entries found.")
            return redirect(
                "/cart/"
            )  # Redirect to cart page or another appropriate page

        last_bill = cust_bill.last()

        total_price = []
        for item in cart_item:
            item.total_price = item.product.price * item.quantity
            item.save()
            total_price.append(item.total_price)

        total_product_price = sum(total_price)

        buy_wallet = Wallet.objects.get(walletuser=request.user)

        # Check if the wallet balance is sufficient
        if buy_wallet.balance < total_product_price:
            messages.error(
                request,
                "Your wallet amount is less than the total amount. Please add funds to your wallet.",
            )
            return render(
                request,
                "bill_confirmation.html",
                {
                    "cart_item": cart_item,
                    "cust_bill": last_bill,
                    "total_ammount": total_product_price,
                    "buy_wallet": buy_wallet,
                },
            )

        return render(
            request,
            "bill_confirmation.html",
            {
                "cart_item": cart_item,
                "cust_bill": last_bill,
                "total_ammount": total_product_price,
                "buy_wallet": buy_wallet,
            },
        )

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred in bill_confirm: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect("/cart/")  # Redirect to cart page or another appropriate page


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    CartItem,
    BillItems,
    BillClone,
    Wallet,
    Product,
)  # Adjust the import based on your actual model location
from decimal import Decimal


def thankyou(request):
    try:
        total_amount = 0
        userid = request.user
        cart_items = CartItem.objects.filter(user_id=userid)

        for item in cart_items:
            final_bill = BillItems.objects.create(
                product=item.product,
                quantity=item.quantity,
                user=item.user,
                total_price=item.total_price,
            )
            final_bill.save()

            total_amount += item.product.price

            product = Product.objects.get(name=item.product)
            print(product.quantity)
            if product.quantity > 0:
                product.quantity -= item.quantity
                product.save()
            else:
                messages.error(request, "Product quantity is less than 0")

            bill_clone = BillClone.objects.create(bill_item=final_bill)
            bill_clone.save()

        buy_wallet = Wallet.objects.get(walletuser=request.user)
        if buy_wallet.balance == 0:
            messages.error(request, "Your wallet has no balance.")
        remaining_amount = buy_wallet.balance - total_amount

        buy_wallet.balance = remaining_amount
        buy_wallet.save()

        cart_items.delete()
        return render(request, "thankyou.html")

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred in thankyou: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect(
            "/cart/"
        )  # Redirect to the cart page or another appropriate page


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
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred in add_funds: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect(
            "/buyer/wallet/"
        )  # Redirect to the wallet page or another appropriate page


def withdraw_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)
                buyer_wallet = Wallet.objects.get(walletuser=request.user)

                if buyer_wallet.balance == 0:
                    messages.error(request, "Your wallet has no balance.")
                    return redirect("/buyer/wallet/")

                if amount > buyer_wallet.balance:
                    messages.error(
                        request, "Withdrawal amount exceeds your wallet balance."
                    )
                    return redirect("/buyer/wallet/")

                buyer_wallet.balance -= amount
                buyer_wallet.save()
                # Add transaction history and other logic as needed
                return redirect("/buyer/wallet/")

        return render(request, "withdraw_funds.html")

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred in withdraw_funds: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect(
            "/buyer/wallet/"
        )  # Redirect to the wallet page or another appropriate page


def buyer_wallet(request):
    try:
        buy_wallet = Wallet.objects.get(walletuser=request.user)
        return render(request, "buyer_wallet.html", {"buy_wallet": buy_wallet})

    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist
        messages.error(request, "Wallet not found.")
        return redirect(
            "/buyer/dashboard/"
        )  # Redirect to the dashboard or another appropriate page


def buyer_dashboard(request):
    try:
        userid = request.user.id
        items = BillItems.objects.filter(user=userid)
        return render(request, "buyer_dashboard.html", {"items": items})

    except Exception as e:
        # Handle exceptions, log the error, and display a generic message
        print(f"An error occurred in buyer_dashboard: {e}")
        messages.error(request, "An error occurred. Please try again.")
        return redirect("/")  # Redirect to the home page or another appropriate page
