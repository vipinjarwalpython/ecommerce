from django.urls import path
from superadmin import views

urlpatterns = [
    path("dashboard/", views.superadmin_dashboard, name="superadmin_dashboard"),
    # path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.superadmin_login, name="superadminlogin"),
    # path("superadmin_register/", views.superadmin_register, name="superadmin_register"),
    path("logout/", views.superadmin_logout, name="superadmin_logout"),
    path("seller_list/", views.seller_list, name="seller_list"),
    path("buyer_list/", views.buyer_list, name="buyer_list"),
    path("product_list/", views.product_list, name="product_list"),
    path(
        "categorywise_productlist/",
        views.categorywise_productlist,
        name="categorywise_productlist",
    ),
    path("sellerwiselist/", views.sellerwise_list, name="sellerwiselist"),
    path("category/<int:id>/", views.product_categorywise, name="product_categorywise"),
    # path(
    #     "Electronicsandmobile/", views.Electronicsandmobile, name="Electronicsandmobile"
    # ),
    # path("Fashionandlifestyle/", views.Fashionandlifestyle, name="Fashionandlifestyle"),
    # path("Media/", views.Media, name="Media"),
    # path("Homeandappliances/", views.Homeandappliances, name="Homeandappliances"),
    # path(
    #     "Homemadeandcraftings/", views.Homemadeandcraftings, name="Homemadeandcraftings"
    # ),
    # path("Footwear/", views.Footwear, name="Footwear"),
    # path("Giftsandhampers/", views.Giftsandhampers, name="Giftsandhampers"),
    # path(
    #     "Festivalshoppingitems/",
    #     views.Festivalshoppingitems,
    #     name="festivalshoppingitems",
    # ),
    path(
        "sellerwiselist_select/<int:id>/",
        views.sellerwiseindividuallist,
        name="sellerwiselist_select",
    ),
    path("superadmin_wallet/", views.superadmin_wallet, name="superadmin_wallet"),
    path(
        "superadmin_add_funds/", views.superadmin_add_funds, name="superadmin_add_funds"
    ),
    path(
        "superadmin_deduct_funds/",
        views.superadmin_withdraw_funds,
        name="superadmin_withdraw_funds",
    ),
    path("walletwise_seller/", views.walletwise_sellerlist, name="walletwise_seller"),
    path("settlement/", views.settlement, name="settlement"),
    path("final_settlement/<int:id>/", views.final_settlement, name="final_settlement"),
    path("dashboard/<int:id>/", views.buyer_dashboard, name="dashboard"),
]
