from django.contrib import admin
from buyer.models import Buyer, CartItem, BuyersBilling, BillItems, BillClone


# Register your models here.


admin.site.register(Buyer)
admin.site.register(CartItem)
admin.site.register(BuyersBilling)
admin.site.register(BillItems)
admin.site.register(BillClone)
