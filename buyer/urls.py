from django.contrib import admin
from django.urls import path, include
from buyer import views

urlpatterns = [
    path("signup/", views.buyer_signup, name="signup"),
    path("login/", views.buyer_login, name="login"),
    path("logout/", views.buyer_logout, name="logout"),
    path("view/", views.view_cart, name="view_cart"),
    path("wallet/", views.buyer_wallet, name="wallet"),
    path("add_funds/", views.add_funds, name="wallet"),
    path("withdraw_funds/", views.withdraw_funds, name="withdraw_funds"),
    path("dashboard/", views.buyer_dashboard, name="dashboard"),
]
