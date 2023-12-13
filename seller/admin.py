from django.contrib import admin
from seller.models import Seller
from seller.models import Product
from seller.models import SellerWallet

# Register your models here.


admin.site.register(Seller)

admin.site.register(Product)

admin.site.register(SellerWallet)
