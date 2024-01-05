from django.urls import path
from .views import (
    SellerSignUpApi,
    SellerLoginApi,
    SellerLogoutApi,
    ProductRegistration,
    ProductUpdate,
    ProductDelete,
    ProductList,
    AddFunds,
    WithdrawFunds,
    SellerWallet,
)

urlpatterns = [
    path("sellersignup/", SellerSignUpApi.as_view(), name="seller_signup"),
    path("sellerlogin/", SellerLoginApi.as_view(), name="seller_login"),
    path("sellerlogout/", SellerLogoutApi.as_view(), name="seller_logout"),
    path("productregister/", ProductRegistration.as_view(), name="product-register"),
    path("productupdate/", ProductUpdate.as_view(), name="product-update"),
    path("productdelete/", ProductDelete.as_view(), name="product-delete"),
    path("productlist/", ProductList.as_view(), name="product-list"),
    path("addfunds/", AddFunds.as_view(), name="add-funds"),
    path("withdrawfunds/", WithdrawFunds.as_view(), name="withdraw-funds"),
    path("sellerwallet/", SellerWallet.as_view(), name="seller_wallet"),
]
