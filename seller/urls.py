from django.urls import path
from seller import views

urlpatterns = [
    path("register/", views.seller_register, name="seller_register"),
    path("login/", views.seller_login, name="seller_login"),
    path("logout/", views.seller_logout, name="seller_logout"),
    path("product/", views.product_registration, name="product_registration"),
    path("update/<int:id>", views.update_product, name="update_product"),
    path(
        "do_update_product/<int:id>", views.do_update_product, name="do_update_product"
    ),
    path("delete/<int:id>", views.delete_product, name="delete_product"),
    path("seller_wallet/", views.seller_wallet, name="seller_wallet"),
    path("add_funds/", views.add_funds, name="add_funds"),
    path("withdraw_funds/", views.withdraw_funds, name="withdraw_funds"),
]
