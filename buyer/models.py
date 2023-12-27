from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from seller.models import Product


# Create your models here.


class Buyer(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="buyer")
    user_type = models.CharField(max_length=10, default="buyer")
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.buyer.first_name}"


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class BuyersBilling(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    address = models.TextField()
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    postal = models.CharField(max_length=32)
    country = models.CharField(max_length=256)
    email = models.CharField(max_length=30)
    phone = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.user}"


class BillItems(models.Model):
    # buyer_details = models.ForeignKey(BuyersBilling, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} : {self.quantity} x {self.product.name}"


class BillClone(models.Model):
    bill_item = models.ForeignKey(BillItems, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bill_item}"
