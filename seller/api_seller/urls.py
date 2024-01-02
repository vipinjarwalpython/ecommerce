from django.urls import path
from .views import SellerSignUpApi, SellerLoginApi

urlpatterns = [
    path("sellersignup/", SellerSignUpApi.as_view(), name="seller_signup"),
    path("sellerlogin/", SellerLoginApi.as_view(), name="seller_login"),
]
