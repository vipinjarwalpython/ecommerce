# Generated by Django 4.2.5 on 2023-12-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='user_type',
            field=models.CharField(choices=[('seller', 'Seller')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
