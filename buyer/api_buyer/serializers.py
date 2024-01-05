from rest_framework import serializers
from buyer.models import *
from superadmin.models import *
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
        return value


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class BuyerBillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyersBilling
        fields = [
            "user",
            "first_name",
            "last_name",
            "address",
            "city",
            "postal",
            "country",
            "email",
            "phone",
            "notes",
        ]


class BillConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItems
        fields = "__all__"


class BuyerWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class BuyerDashBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItems
        fields = "__all__"
