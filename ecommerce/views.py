from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def aboutus(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")


def blog(request):
    return render(request, "blog.html")


def contactus(request):
    return render(request, "contact.html")


<<<<<<< HEAD
def checkout(request):
    return render(request, "checkout.html")
=======
def cart(request):
    return render(request, "cart.html")




>>>>>>> 31f591ef7f1ab533cb04fff180c34db811157ce1
