from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Seller(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    seller_mobilenumber = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.seller.first_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="media/")

    def __str__(self):
        return self.name
