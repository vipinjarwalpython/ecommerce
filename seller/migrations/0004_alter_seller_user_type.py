# Generated by Django 4.2.8 on 2023-12-21 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_seller_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='user_type',
            field=models.CharField(default='seller', max_length=10),
        ),
    ]
