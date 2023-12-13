from django.contrib import admin
from django.urls import path, include
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from seller import views as productview
from buyer import views as buyer_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    # path("shop/", views.shop, name="shop"),
    path("shop/", productview.product_list, name="product-list"),
    path("about/", views.aboutus, name="aboutus"),
    path("services/", views.services, name="services"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contactus, name="contactus"),
    path("seller/", include("seller.urls")),
    # path("", include("buyer.urls")),
    path("cart/", buyer_views.view_cart, name="cart"),
    path("add/<int:id>/", buyer_views.add_to_cart, name="add_to_cart"),
    path("remove/<int:id>/", buyer_views.remove_from_cart, name="remove_from_cart"),
    path("plus/<int:id>/", buyer_views.plus_to_cart, name="plus_to_cart"),
    path("minus/<int:id>/", buyer_views.minus_from_cart, name="minus_from_cart"),
    path("bill/", buyer_views.billing, name="billing"),
    path("buyer/", include("buyer.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
