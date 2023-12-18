from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class SuperAdmin(models.Model):
    superadmin = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.superadmin.username


# Create your models here.


class SuperAdminWallet(models.Model):
    superuser = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)




