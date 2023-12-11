from django.urls import path
from seller import views

urlpatterns = [
    path("register/", views.seller_register, name="seller_register"),
    path("login/", views.seller_login, name="seller_login"),
    path("logout/", views.seller_logout, name="seller_logout"),
    path("product/", views.product_registration, name="product_registration"),
]
