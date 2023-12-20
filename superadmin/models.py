from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class SuperAdmin(models.Model):
    superadmin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.superadmin.username


# Create your models here.


class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=2, max_digits=10)
    walletuser = models.OneToOneField(User, on_delete=models.CASCADE)
