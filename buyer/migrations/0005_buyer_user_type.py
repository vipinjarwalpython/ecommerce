# Generated by Django 4.2.8 on 2023-12-21 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer', '0004_alter_cartitem_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='user_type',
            field=models.CharField(choices=[('buyer', 'Buyer')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
