from django.contrib import admin
from django.urls import path, include
from ecommerce import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("about/", views.aboutus, name="aboutus"),
    path("services/", views.services, name="services"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contactus, name="contactus"),
    path("cart/", views.cart, name="cart"),
    path("buyer/", include("buyer.urls")),
    # path("admin/", admin.site.urls),
]
