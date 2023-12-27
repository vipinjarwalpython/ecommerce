from rest_framework import serializers
from buyer.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "password"]


class BuyerSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()

    class Meta:
        model = Buyer
        fields = ["id", "user_type", "phone", "buyer"]

    # def create(self, validated_data):
    #     buyer = validated_data.pop("buyer")
    #     buyer_user = User.objects.create(**validated_data)
    #     for buy in buyer:
    #         Buyer.objects.create(user=buyer_user, **buy)
    #     return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
