from superadmin.api_superadmin.serializers import (
    UserSerializer,
    SuperAdminSerializer,
    WalletSerializer,
)
from superadmin.models import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from seller.models import Seller, Category, Product
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes
from superadmin.models import Wallet
from decimal import Decimal
from rest_framework.response import Response
from buyer.models import Buyer
from seller.api_seller.serializers import (
    SellerSerializer,
    ProductSerializer,
    CategorySerializer,
    WalletSerializer,
)


class SuperAdminDashboard(APIView):
    def post(self, request):
        try:
            # seller_serializer = SellerSerializer(seller, many=True)
            # print(seller_serializer.data)
            data = request.data
            print(data)

            seller = Product.objects.all()
            print(seller)

            id = data.get("productid")
            product = Product.objects.get(id=id)
            print(product)

            if product.approved:
                product.approved = False
                product.save()
                print("if part")
            else:
                product.approved = True
                product.save()
                print("else part")
                # buyers= Buyer.objects.all()
                # buyer_serializer = UserSerializer()
            seller = Seller.objects.all()
            print(seller)
            seller_serializer = SellerSerializer(seller, many=True)
            product = Product.objects.all()
            product_serializer = ProductSerializer(product, many=True)
            category = Category.objects.all()
            category_serializer = CategorySerializer(category, many=True)
            context = {
                "sellerserilizer": seller_serializer.data,
                "productserializer": product_serializer.data,
                "categoryserializer": category_serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminLogin(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data)
            user = User.objects.filter(username=data["username"])
            print(user)
            if not user.exists():
                context = {
                    "message": "username not found",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND,
                }
                return Response(context)
            superadmin = authenticate(
                request, username=data["username"], password=data["password"]
            )
            print(superadmin)
            if superadmin is None:
                context = {
                    "message": "password incorrect",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND,
                }
            else:
                login(request, superadmin)
                refresh_token = RefreshToken.for_user(superadmin)
                token = {
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                }

                context = (
                    {
                        "message": f"Welcome {superadmin} , you are logged in",
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "token": token,
                    },
                )
            return Response(context)
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminLogout(APIView):
    def get(self, request):
        try:
            logout(request)
            context = {
                "message": "You are successfully logged out",
                "success": True,
                "status": status.HTTP_200_OK,
            }
            return Response(context)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminAddFunds(APIView):
    def post(self, request):
        try:
            data = request.data
            amount = data.get("amount")

            if amount is not None:
                amount = Decimal(amount)

                superadmin_wallet = Wallet.objects.get(walletuser=request.user)
                superadmin_wallet.balance += amount
                superadmin_wallet.save()

                # Use the serializer to get the serialized data for the response
                superadmin_wallet_serializer = WalletSerializer(superadmin_wallet)
                context = {
                    "message": "success",
                    "superadmin_wallet": superadmin_wallet_serializer.data,
                }

                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Amount cannot be None"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminWithdrawFunds(APIView):
    def post(self, request):
        try:
            data = request.data
            amount = data.get("amount")

            if amount is not None:
                amount = Decimal(amount)

                superadmin_wallet = Wallet.objects.get(walletuser=request.user)
                superadmin_wallet.balance -= amount
                if superadmin_wallet.balance <= 0:
                    context = {"message": "balance insufficient"}
                    return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    superadmin_wallet.save()

                    # Use the serializer to get the serialized data for the response
                    superadmin_wallet_serializer = WalletSerializer(superadmin_wallet)
                    context = {
                        "message": "success",
                        "superadmin_wallet": superadmin_wallet_serializer.data,
                    }

                    return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SuperAdminWallet(APIView):
    def get(self, request):
        try:
            superadmin_wallet = Wallet.objects.get(walletuser=request.user)
            superadminwallet = WalletSerializer(superadmin_wallet)
            print(superadminwallet)
            context = {
                "message": "success",
                "superadmin_wallet": superadminwallet.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WalletWiseSellerList(APIView):
    def get(self, request):
        try:
            sellers = Seller.objects.all()
            wallets = Wallet.objects.filter(user_type="seller")
            seller_serializer = SellerSerializer(sellers, many=True)
            print(seller_serializer.data)
            wallet_serializer = WalletSerializer(wallets, many=True)
            print(wallet_serializer.data)
            context = {
                "seller_serializer": seller_serializer.data,
                "wallet_serilizer": wallet_serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)
