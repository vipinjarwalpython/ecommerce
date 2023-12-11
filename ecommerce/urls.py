from django.contrib import admin
from django.urls import path, include
from ecommerce import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("about/", views.aboutus, name="aboutus"),
    path("services/", views.services, name="services"),
    path("blog/", views.blog, name="blog"),
    path("contact/", views.contactus, name="contactus"),
    path("seller/", include("seller.urls")),
    # path("", include("buyer.urls")),
    path("cart/", views.cart, name="cart"),
    path("buyer/", include("buyer.urls")),
    # path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()
