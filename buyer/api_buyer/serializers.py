from rest_framework import serializers
from buyer.models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]

    def validate_email(self, value):
        # Add additional email validation logic if needed
        return value

    def validate_password(self, value):
        # Add additional password validation logic if needed
        return value


class BuyerSerializer(serializers.ModelSerializer):
    buyer = UserSerializer()

    phone = serializers.CharField(
        required=True,
        max_length=10,  # Example: Phone number must be 10 digits
    )

    class Meta:
        model = Buyer
        fields = ["id", "user_type", "phone", "buyer"]

    def validate_phone(self, value):
        # Add additional phone validation logic if needed
        return value


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
