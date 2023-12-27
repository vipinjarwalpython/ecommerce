from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from seller.models import Seller, Product

from decimal import Decimal
from django.contrib.auth.decorators import login_required
from seller.models import Category
from superadmin.models import Wallet

# Create your views here.


def seller_register(request):
    try:
        if request.method == "POST":
            seller_firstname = request.POST.get("seller_firstname")
            seller_lastname = request.POST.get("seller_lastname")
            seller_email = request.POST.get("seller_email")
            seller_mobilenumber = request.POST.get("seller_mobilenumber")
            seller_username = request.POST.get("seller_username")
            seller_password1 = request.POST.get("seller_password1")
            seller_password2 = request.POST.get("seller_password2")

            if seller_password1 != seller_password2:
                messages.error(request, "Passwords do not match")
                return redirect("/seller/register/")

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

            Wallet.objects.create(walletuser=user, balance=0, user_type="seller")
            user.save()

            return redirect("/seller/login/")

    except Exception as e:
        # Log the exception or handle it as needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/seller/register/")

    return render(request, "seller_register.html")


def seller_login(request):
    try:
        if request.method == "POST":
            seller_username = request.POST.get("seller_username")
            seller_password = request.POST.get("seller_password")
            user_seller = User.objects.get(username=seller_username)

            if not Seller.objects.filter(seller_id=user_seller.id).exists():
                messages.error(request, "Invalid username or password")
                return redirect("/seller/login/")

            user = authenticate(username=seller_username, password=seller_password)
            if user is None:
                messages.error(request, "Invalid username or password")
            else:
                login(request, user)
                return redirect("/seller/product/")

    except User.DoesNotExist:
        # Handle the case where the user does not exist
        messages.error(request, "Invalid username or password")
        return redirect("/seller/login/")

    except Exception as e:
        # Log the exception or handle it as needed
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("/seller/login/")

    return render(request, "seller_login.html")


def seller_logout(request):
    try:
        logout(request)
        return redirect("/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during seller logout: {str(e)}")
        return redirect("/seller-logout-error/")


@login_required(login_url="/seller/login/")
def dashboard(request):
    try:
        return render(request, "sellerdashboard.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while accessing the seller dashboard: {str(e)}")
        return redirect("/seller-dashboard-error/")


@login_required(login_url="/seller/login/")
def product_registration(request):
    try:
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
                quantity = request.POST.get("quantity")
                categoryid = request.POST.get("category")

                # Create a Product instance associated with the Seller
                product = Product.objects.create(
                    seller=seller_instance,
                    name=name,
                    description=description,
                    price=price,
                    image=image,
                    quantity=quantity,
                    approved=False,
                    category_id=categoryid,
                )
                print(product.approved)
                # Check for admin approval or custom approval process
        userid = request.user

        seller = Seller.objects.get(seller=userid)

        products = Product.objects.filter(seller=seller)
        return render(request, "product_registration.html", {"products": products})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during product registration: {str(e)}")
        return redirect("/product-registration-error/")


@login_required(login_url="/seller/login/")
def update_product(request, id):
    try:
        product = Product.objects.get(pk=id)
        category = Category.objects.all()
        return render(
            request, "update_product.html", {"product": product, "category": category}
        )

    except Product.DoesNotExist:
        # Handle the case where the product with the specified ID does not exist
        print(f"Product with id {id} does not exist.")
        return redirect("/update-product-error/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during product update: {str(e)}")
        return redirect("/update-product-error/")


@login_required(login_url="/seller/login/")
def do_update_product(request, id):
    try:
        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            price = request.POST.get("price")
            image = request.FILES.get("image")
            quantity = request.POST.get("quantity")
            categoryid = request.POST.get("category")

            product = Product.objects.get(pk=id)

            if image:
                product.image = image
                product.save()
                return redirect("/seller/product/")

            product.name = name
            product.description = description
            product.price = price
            product.quantity = quantity
            new_category = Category.objects.get(id=categoryid)
            product.category = new_category
            product.save()

            return redirect("/seller/product/")

    except Product.DoesNotExist:
        # Handle the case where the product with the specified ID does not exist
        print(f"Product with id {id} does not exist.")
        return redirect("/update-product-error/")

    except Category.DoesNotExist:
        # Handle the case where the category with the specified ID does not exist
        print(f"Category with id {categoryid} does not exist.")
        return redirect("/update-product-error/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during product update: {str(e)}")
        return redirect("/update-product-error/")


@login_required(login_url="/seller/login/")
def delete_product(request, id):
    try:
        product = Product.objects.get(pk=id)
        product.delete()
        return redirect("/seller/product/")

    except Product.DoesNotExist:
        # Handle the case where the product with the specified ID does not exist
        print(f"Product with id {id} does not exist.")
        return redirect("/delete-product-error/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during product deletion: {str(e)}")
        return redirect("/delete-product-error/")


@login_required(login_url="/seller/login/")
def product_list(request):
    try:
        products = Product.objects.filter(approved=True)
        return render(request, "shop.html", {"products": products})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the product list: {str(e)}")
        return render(request, "error_page.html")


@login_required(login_url="/seller/login/")
def add_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)

                seller_wallet = Wallet.objects.get(walletuser=request.user)
                seller_wallet.balance += amount
                seller_wallet.save()
                # Add transaction history and other logic as needed
                return redirect("/seller/seller_wallet/")

        return render(request, "add_funds.html")

    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist for the user
        print(f"Wallet not found for user {request.user}.")
        return render(request, "wallet_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during fund addition: {str(e)}")
        return redirect("/add-funds-error/")


@login_required(login_url="/seller/login/")
def withdraw_funds(request):
    try:
        if request.method == "POST":
            amount = request.POST.get("amount")
            if amount is not None:
                amount = Decimal(amount)

                seller_wallet = Wallet.objects.get(walletuser=request.user)
                seller_wallet.balance -= amount
                seller_wallet.save()
                # Add transaction history and other logic as needed
                return redirect("/seller/seller_wallet/")

        return render(request, "withdraw_funds.html")

    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist for the user
        print(f"Wallet not found for user {request.user}.")
        return render(request, "wallet_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during fund withdrawal: {str(e)}")
        return redirect("/withdraw-funds-error/")


@login_required(login_url="/seller/login/")
def seller_wallet(request):
    try:
        seller_wallet = Wallet.objects.get(walletuser=request.user)
        return render(request, "seller_wallet.html", {"seller_wallet": seller_wallet})

    except Wallet.DoesNotExist:
        # Handle the case where the wallet does not exist for the user
        print(f"Wallet not found for user {request.user}.")
        return render(request, "wallet_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the seller wallet: {str(e)}")
        return render(request, "wallet_error.html")
