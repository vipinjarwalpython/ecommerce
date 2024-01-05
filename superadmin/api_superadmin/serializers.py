from rest_framework import serializers
from superadmin.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SuperAdminSerializer(serializers.ModelSerializer):
    superadmin = UserSerializer()

    class Meta:
        model = SuperAdmin
        fields = "__all__"


class WalletSerializer(serializers.ModelSerializer):
    walletuser = UserSerializer()

    class Meta:
        model = Wallet
        fields = "__all__"


