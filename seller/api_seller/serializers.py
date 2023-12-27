from rest_framework import serializers
from seller.models import Category, Seller, Product
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    seller = UserSerializer()

    class Meta:
        model = Seller
        fields = ["id",  "user_type", "seller_mobilenumber", "seller"]


# class ProductSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             "seller",
#             "category",
#             "name",
#             "description",
#             "price",
#             "image",
#             "quantity",
#             "approved",
#         ]
