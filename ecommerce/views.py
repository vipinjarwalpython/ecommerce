from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def shop(request):
    return render(request, "shop.html")


def aboutus(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def blog(request):
    return render(request, "blog.html")


def contactus(request):
    return render(request, "contact.html")


def cart(request):
    return render(request, "cart.html")




