from django.urls import path
from buyer.api_buyer.views import (
    BuyerSignupApi,
    BuyerLoginApi,
    BuyerLogoutView,
    CartView,
    AddToCartView,
    RemoveToCartView,
    PlusToCartView,
    MinusToCartView,
    BillingView,
    BillConfirmView,
    ThankyouView,
    AddFundView,
    WithdrawFundView,
    BuyerWalletView,
    BuyerDashBoardView,
)


urlpatterns = [
    path("signup/", BuyerSignupApi.as_view()),
    path("login/", BuyerLoginApi.as_view()),
    path("logout/", BuyerLogoutView.as_view()),
    path("cartitem/", CartView.as_view()),
    path("additem/", AddToCartView.as_view()),
    path("removeitem/", RemoveToCartView.as_view()),
    path("plusitem/", PlusToCartView.as_view()),
    path("minusitem/", MinusToCartView.as_view()),
    path("billing/", BillingView.as_view()),
    path("billing-confirm/", BillConfirmView.as_view()),
    path("thankyou/", ThankyouView.as_view()),
    path("add-fund/", AddFundView.as_view()),
    path("withdraw-fund/", WithdrawFundView.as_view()),
    path("buyer-wallet/", BuyerWalletView.as_view()),
    path("buyer-dashboard/", BuyerDashBoardView.as_view()),
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
]
