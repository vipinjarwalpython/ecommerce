# Generated by Django 4.2.8 on 2023-12-19 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0013_product_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SellerWallet',
        ),
    ]
