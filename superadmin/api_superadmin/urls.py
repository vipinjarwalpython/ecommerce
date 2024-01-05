from django.urls import path
from .views import (
    SuperAdminDashboard,
    SuperAdminLogin,
    SuperAdminLogout,
    SuperAdminAddFunds,
    SuperAdminWithdrawFunds,
    SuperAdminWallet,
    WalletWiseSellerList,
)

urlpatterns = [
    path(
        "superadmindashboard/",
        SuperAdminDashboard.as_view(),
        name="superadmin-dashboard",
    ),
    path(
        "superadminlogin/",
        SuperAdminLogin.as_view(),
        name="superadmin-login",
    ),
    path(
        "superadminlogout/",
        SuperAdminLogout.as_view(),
        name="superadmin-login",
    ),
    path(
        "superadminaddfund/",
        SuperAdminAddFunds.as_view(),
        name="superadmin-add-funds",
    ),
    path(
        "superadminwithdrawfund/",
        SuperAdminWithdrawFunds.as_view(),
        name="superadmin-funds-withdrawal",
    ),
    path(
        "superadminwallet/",
        SuperAdminWallet.as_view(),
        name="superadmin-wallet",
    ),
    path(
        "walletwisesellerlist/",
        WalletWiseSellerList.as_view(),
        name="walletwise-sellerlist",
    ),
]
