from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Seller(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_mobilenumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.seller.first_name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="media/")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SellerWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
