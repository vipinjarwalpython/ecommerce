from django.urls import path
from buyer.api_buyer.views import BuyerApi, BuyerSignupApi, BuyerLoginApi, CartItemApi
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("buyersignup/", BuyerSignupApi.as_view()),
    path("buyerlogin/", BuyerLoginApi.as_view()),
    path("buyer-details-show/", BuyerApi.as_view()),
    path("buyer-details-show/<int:id>/", BuyerApi.as_view()),
    path(
        "buyersignup/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "buyersignup/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("buyersignup/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("cartitem/", CartItemApi.as_view()),
]
