from django.urls import path
from superadmin import views

urlpatterns = [
    path("dashboard/", views.superadmin_dashboard, name="superadmin_dashboard"),
    # path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.superadmin_login, name="superadminlogin"),
    # path("superadmin_register/", views.superadmin_register, name="superadmin_register"),
    path("logout/", views.superadmin_logout, name="superadmin_logout"),
    path("seller_list/", views.seller_list, name="seller_list"),
    path("product_list/", views.product_list, name="product_list"),
    path(
        "categorywise_productlist/",
        views.categorywise_productlist,
        name="categorywise_productlist",
    ),
]
