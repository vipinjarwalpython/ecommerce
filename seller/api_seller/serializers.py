from rest_framework import serializers
from seller.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    seller = UserSerializer()

    class Meta:
        model = Seller
        fields = "__all__"
