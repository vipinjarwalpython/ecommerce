from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    SellerSerializer,
    ProductSerializer,
    WalletSerializer,
)
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


class SellerSignUpApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save(
                    password=make_password(data.get("password")),
                    is_active=True,
                )
                seller_mobilenumber = data.get("seller_mobilenumber")
                print(user.id)
                print(seller_mobilenumber)
                seller_obj = Seller.objects.create(
                    seller=user, seller_mobilenumber=seller_mobilenumber
                )
                seller = Seller.objects.get(seller=user)
                print(seller)

                if seller_obj is not None:
                    seller_serializer = SellerSerializer(seller)
                    refresh_token = RefreshToken.for_user(user)
                    token = {
                        "refresh": str(refresh_token),
                        "access": str(refresh_token.access_token),
                    }
                    print(seller_serializer.data)
                    return Response(
                        {
                            "msg": "Data Created",
                            "seller_serializer": seller_serializer.data,
                            "token": token,
                        },
                        status=status.HTTP_201_CREATED,
                    )

                else:
                    user.delete()
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


class SellerLoginApi(APIView):
    def post(self, request, *args, **kwargs):
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
            seller = authenticate(
                request, username=data["username"], password=data["password"]
            )
            print(seller)
            if seller is None:
                context = {
                    "message": "password incorrect",
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND,
                }
            else:
                login(request, seller)
                refresh_token = RefreshToken.for_user(seller)
                token = {
                    "refresh": str(refresh_token),
                    "access": str(refresh_token.access_token),
                }

                context = (
                    {
                        "message": f"Welcome {seller} , you are logged in",
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "token": token,
                    },
                )
            return Response(context)
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class SellerLogoutApi(APIView):
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


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class ProductRegistration(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            print("===================================")
            user = request.user
            print(user.id)

            print(data.get("categoryid"))
            category = Category.objects.get(id=data.get("categoryid"))
            print("===========================================")
            print(category)
            seller_instance = Seller.objects.get(
                seller=user,
            )
            print(seller_instance)
            product = Product.objects.create(
                seller=seller_instance,
                category=category,
                name=data["name"],
                description=data["description"],
                price=int(data["price"]),
                image=data["image"],
                quantity=int(data["quantity"]),
                approved=data.get("approved", False),
            )
            print(product)
            # userid = request.user

            # seller = Seller.objects.get(seller=userid)

            # products = Product.objects.filter(seller=seller)
            return Response({"msg": "product registerd"})
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdate(APIView):
    def post(self, request):
        try:
            data = request.data
            user = request.user
            print(data.get("categoryid"))
            categoryid = Category.objects.get(id=data.get("category"))
            print("===========================================")
            print(categoryid)
            seller_instance = Seller.objects.get(
                seller=user,
            )
            product = Product.objects.get(id=data.get("productid"))

            print(product)
            print("=============================================")

            product.seller = seller_instance
            product.category = categoryid
            product.name = data["name"]
            product.description = data["description"]
            product.price = int(data["price"])
            product.image = data["image"]
            product.quantity = int(data["quantity"])
            product.approved = data.get("approved", False)

            product.save()

            print("+++++++++++++++++++++++++++++++++++++++")
            print(product)
            context = {"message": "Success"}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductDelete(APIView):
    def get(self, request):
        try:
            data = request.data
            product = Product.objects.get(id=data.get("productid"))
            print(product)
            product.delete()
            print("=============================================")
            context = {"message": "Success"}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(approved=True)
            product_serializer = ProductSerializer(products, many=True)
            print("+++++++++++++++++++++++++++++++++++++")
            print(product_serializer)
            serialized_data = product_serializer.data  # Extract serialized data
            print(serialized_data)
            context = {"message": "success", "product": serialized_data}
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddFunds(APIView):
    def post(self, request):
        try:
            data = request.data
            amount = data.get("amount")

            if amount is not None:
                amount = Decimal(amount)

                seller_wallet = Wallet.objects.get(walletuser=request.user)
                seller_wallet.balance += amount
                seller_wallet.save()

                # Use the serializer to get the serialized data for the response
                seller_wallet_serializer = WalletSerializer(seller_wallet)
                context = {
                    "message": "success",
                    "seller_wallet": seller_wallet_serializer.data,
                }

                return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WithdrawFunds(APIView):
    def post(self, request):
        try:
            data = request.data
            amount = data.get("amount")

            if amount is not None:
                amount = Decimal(amount)

                seller_wallet = Wallet.objects.get(walletuser=request.user)
                seller_wallet.balance -= amount
                if seller_wallet.balance <= 0:
                    context = {"message": "balance insufficient"}
                    return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    seller_wallet.save()

                    # Use the serializer to get the serialized data for the response
                    seller_wallet_serializer = WalletSerializer(seller_wallet)
                    context = {
                        "message": "success",
                        "seller_wallet": seller_wallet_serializer.data,
                    }

                return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SellerWallet(APIView):
    def get(self, request):
        try:
            seller_wallet = Wallet.objects.get(walletuser=request.user)
            sellerwallet = WalletSerializer(seller_wallet)
            print(sellerwallet)
            context = {
                "message": "success",
                "seller_wallet": sellerwallet.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 






