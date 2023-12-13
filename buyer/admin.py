from django.contrib import admin
from buyer.models import Buyer, CartItem, BuyerBilling

# Register your models here.


admin.site.register(Buyer)
admin.site.register(CartItem)
admin.site.register(BuyerBilling)
