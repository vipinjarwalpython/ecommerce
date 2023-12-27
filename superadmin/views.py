from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from buyer.models import Buyer, BillClone, BillItems
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


@login_required(login_url="/superadmin/login/")
def superadmin_dashboard(request):
    try:
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

        return render(
            request,
            "superadmin_dashboard.html",
            {
                "buyers": buyers,
                "seller": seller,
                "product": product,
                "category": category,
            },
        )

    except Product.DoesNotExist:
        # Handle the case where the product with the specified ID does not exist
        print(f"Product with id {id} does not exist.")
        # return render(request, "product_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred in the superadmin dashboard: {str(e)}")
        return render(request, "superadmin_dashboard_error.html")


def superadmin_login(request):
    try:
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

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during superadmin login: {str(e)}")
        return render(request, "superadmin_login_error.html")


@login_required(login_url="/superadmin/login/")
def superadmin_logout(request):
    try:
        logout(request)
        return redirect("/")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during superadmin logout: {str(e)}")
        return render(request, "superadmin_logout_error.html")


@login_required(login_url="/superadmin/login/")
def seller_list(request):
    try:
        sellers = Seller.objects.all()
        return render(request, "seller_list.html", {"sellers": sellers})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the seller list: {str(e)}")
        return render(request, "seller_list_error.html")


@login_required(login_url="/superadmin/login/")
def buyer_list(request):
    try:
        buyers = Buyer.objects.all()
        return render(request, "buyer_list.html", {"buyers": buyers})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the buyer list: {str(e)}")
        return render(request, "buyer_list_error.html")


@login_required(login_url="/superadmin/login/")
def product_list(request):
    try:
        product = Product.objects.all()
        return render(request, "product_list.html", {"product": product})
    except Exception as e:
        print(f"An error occurred: {e}")
        return render(request, "error_page.html")


@login_required(login_url="/superadmin/login/")
def sellerwise_list(request):
    try:
        sellers = Seller.objects.all()
        return render(request, "sellerwiselist.html", {"sellers": sellers})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the seller-wise list: {str(e)}")
        return render(request, "sellerwise_list_error.html")


@login_required(login_url="/superadmin/login/")
def sellerwiseindividuallist(request, id):
    try:
        seller = get_object_or_404(Seller, pk=id)
        product = Product.objects.filter(seller=seller)
        return render(request, "sellerwiselist_select.html", {"product": product})

    except Exception as e:
        # Log the exception or handle it as needed
        print(
            f"An error occurred while retrieving the seller-wise individual list: {str(e)}"
        )
        return render(request, "sellerwise_individual_list_error.html")


@login_required(login_url="/superadmin/login/")
def categorywise_productlist(request):
    try:
        categories = Category.objects.all()
        return render(
            request, "categorywise_productlist.html", {"categories": categories}
        )

    except Exception as e:
        # Log the exception or handle it as needed
        print(
            f"An error occurred while retrieving the category-wise product list: {str(e)}"
        )
        return render(request, "categorywise_productlist_error.html")


@login_required(login_url="/superadmin/login/")
def product_categorywise(request, id):
    try:
        category = get_object_or_404(Category, id=id)
        product = Product.objects.filter(category=category)
        return render(request, "category_product.html", {"product": product})

    except Exception as e:
        # Log the exception or handle it as needed
        print(
            f"An error occurred while retrieving the category-wise product list: {str(e)}"
        )
        return render(request, "categorywise_product_error.html")


@login_required(login_url="/superadmin/login/")
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


@login_required(login_url="/superadmin/login/")
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


@login_required(login_url="/superadmin/login/")
def superadmin_wallet(request):
    try:
        superadmin_wallet = get_object_or_404(Wallet, walletuser=request.user)
        return render(
            request, "superadmin_wallet.html", {"superadmin_wallet": superadmin_wallet}
        )

    except Http404:
        # Handle the case where the Wallet does not exist
        return render(request, "superadmin_wallet_not_found.html")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the superadmin wallet: {str(e)}")
        return render(request, "superadmin_wallet_error.html")


@login_required(login_url="/superadmin/login/")
def walletwise_sellerlist(request):
    try:
        sellers = Seller.objects.all()
        wallets = Wallet.objects.filter(user_type="seller")
        return render(
            request,
            "walletwise_sellerlist.html",
            {"sellers": sellers, "wallets": wallets},
        )

    except Exception as e:
        # Log the exception or handle it as needed
        print(
            f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
        )
        return render(request, "walletwise_sellerlist_error.html")


@login_required(login_url="/superadmin/login/")
def settlement(request):
    try:
        billclone = BillClone.objects.all()
        return render(request, "settlement.html", {"billclone": billclone})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving the settlement data: {str(e)}")
        return render(request, "settlement_error.html")


@login_required(login_url="/superadmin/login/")
def final_settlement(request, id):
    try:
        billclone = BillClone.objects.get(id=id)

        # Send Money from buyer wallet to seller wallet, deducting 95% of the total bill with individual product prices
        seller_wallet = Wallet.objects.get(
            walletuser_id=billclone.bill_item.product.seller.seller.id
        )
        seller_wallet.balance += Decimal((billclone.bill_item.total_price * 95) / 100)
        seller_wallet.save()

        # Send Money from buyer wallet to superadmin wallet, 5% of the total bill with individual product prices
        superadmin_wallet = Wallet.objects.get(user_type="superadmin")
        superadmin_wallet.balance += Decimal(
            (billclone.bill_item.total_price * 5) / 100
        )
        superadmin_wallet.save()

        billclone.delete()

        return render(request, "final-settlement.html")

    except BillClone.DoesNotExist:
        # Handle the case where the BillClone with the specified ID does not exist
        raise Http404("BillClone does not exist")

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred during final settlement: {str(e)}")
        return render(request, "final_settlement_error.html")


@login_required(login_url="/superadmin/login/")
def buyer_dashboard(request, id):
    try:
        items = BillItems.objects.filter(user_id=id)
        print(items)
        return render(request, "buyer_dashboard_super.html", {"items": items})

    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while retrieving buyer dashboard data: {str(e)}")
        return render(request, "buyer_dashboard_error.html")
