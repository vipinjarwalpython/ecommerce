from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Create your models here.


class Seller(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_mobilenumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.seller.first_name


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="media/")
    quantity = models.IntegerField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


