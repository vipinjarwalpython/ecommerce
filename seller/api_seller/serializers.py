from rest_framework import serializers
from seller.models import *
from django.contrib.auth.models import User
from superadmin.models import Wallet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    seller = UserSerializer()

    class Meta:
        model = Seller
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    walletuser = UserSerializer()

    class Meta:
        model = Wallet
        fields = "__all__"
