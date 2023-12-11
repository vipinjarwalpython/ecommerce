from django.contrib import admin
from django.urls import path, include
from buyer import views

urlpatterns = [
    path("signup/", views.buyer_signup, name="signup"),
    path("login/", views.buyer_login, name="login"),
    path("logout/", views.buyer_logout, name="logout"),
    # path("admin/", admin.site.urls),
]
