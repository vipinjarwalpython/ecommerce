# Generated by Django 4.2.8 on 2023-12-12 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0003_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
    ]
