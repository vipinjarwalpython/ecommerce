from django.urls import path
from buyer.api_buyer.views import BuyerSignupApi, BuyerLoginApi
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("signup/", BuyerSignupApi.as_view()),
    path("login/", BuyerLoginApi.as_view()),
    # path("buyer-details-show/", BuyerApi.as_view()),
    # path("buyer-details-show/<int:id>/", BuyerApi.as_view()),
    # path(
    #     "signup/",
    #     jwt_views.TokenObtainPairView.as_view(),
    #     name="token_obtain_pair",
    # ),
    # path(
    #     "buyersignup/refresh/",
    #     jwt_views.TokenRefreshView.as_view(),
    #     name="token_refresh",
    # ),
    # path("buyersignup/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # # path("cartitem/", CartItemApi.as_view()),
]
