from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Buyer, CartItem, BuyerBilling, BillItems
from seller.models import Product

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

            buyer_extra_fields = Buyer.objects.create(
                buyer=buyer,
                phone=phone,
            )

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

        buyer = authenticate(username=username, password=password)
        print(buyer)

        if buyer is None:
            messages.error(request, "password is incorrect")
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
    # print(cart_items)
    # print(cart_items)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        item.save()

        total_price.append(item.total_price)
        # price = CartItem.objects.get(total_price=raw_price)
        # print(price)
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

        print(cart_item, first_name, last_name)

        cust_bill = BuyerBilling.objects.create(
            cart_item=cart_item,
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
    total_ammount = 0
    for item in cart_item:
        total_ammount += item.product.price
        # bill = BuyerBilling.objects.all()
    return render(
        request,
        "checkout.html",
        {"cart_item": cart_item, "total_ammount": total_ammount},
    )

def bill_confirm(request):
    userid = request.user
    cart_item = CartItem.objects.filter(user_id=userid)
    # print(cart_item)
    cust_bill = BuyerBilling.objects.filter(user = userid)
    print(cust_bill)
    print(cust_bill[len(cust_bill)-1])
    

    return render(request, 'bill_confirmation.html', {'cart_item':cart_item, 'cust_bill':cust_bill[len(cust_bill)-1]})


def thankyou(request):
    userid = request.user
    cart_item = CartItem.objects.filter(user_id=userid)
    print(cart_item)
    for item in cart_item:
        print(item)
        final_bill = BillItems.objects.create(
            product=item.product
        )
    # cust_bill = BuyerBilling.objects.get(user = userid)
    # cart_item.delete()
    # cust_bill.delete()


    return render(request, "thankyou.html")