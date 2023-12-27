from django.urls import path

from seller.api_seller.views import (
    CategoryView,
    SellerView,
    SellerSignupApi,
    SellerLoginApi,
    SellerLogoutApi,
)
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("categoryapi/", CategoryView.as_view(), name="category-list"),
    path("categoryapi/<int:id>/", CategoryView.as_view(), name="category-detail"),
    path("sellerapi/", SellerView.as_view(), name="seller-list"),
    path("sellerapi/<int:id>/", SellerView.as_view(), name="seller-detail"),
    path("sellersignup/", SellerSignupApi.as_view(), name="seller-signup"),
    path("sellerlogin/", SellerLoginApi.as_view(), name="seller-login"),
    path("sellerlogout/", SellerLogoutApi.as_view(), name="seller-logout"),
    path(
        "sellerapi/token/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "sellerapi/token/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
