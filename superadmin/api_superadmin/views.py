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
from buyer.models import Buyer, BillClone, BillItems
from seller.api_seller.serializers import (
    SellerSerializer,
    ProductSerializer,
    CategorySerializer,
    WalletSerializer,
)
from buyer.api_buyer.serializers import (
    BuyerSerializer,
    BillCloneSerializer,
    BillConfirmSerializer,
    BuyerDashBoardSerializer,
)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SellerListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            seller = Seller.objects.all()
            serializer = SellerSerializer(seller, many=True)
            seller_list = serializer.data
            context = {"status": status.HTTP_200_OK, "seller_list": seller_list}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BuyerListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            buyer = Buyer.objects.all()
            serializer = BuyerSerializer(buyer, many=True)
            buyer_list = serializer.data
            context = {"status": status.HTTP_200_OK, "buyer_list": buyer_list}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.all()
            serializer = ProductSerializer(product, many=True)
            product_list = serializer.data
            context = {"status": status.HTTP_200_OK, "product_list": product_list}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SellerWiseProductListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.data
            seller = Seller.objects.get(seller_id=user.get("id"))
            product = Product.objects.filter(seller=seller)
            print(product)
            serializer = ProductSerializer(product, many=True)
            product_list = serializer.data
            context = {"status": status.HTTP_200_OK, "product_list": product_list}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CategoryWiseProductListView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.data
            category = Category.objects.get(id=user.get("id"))
            product = Product.objects.filter(category=category)
            print(product)
            serializer = ProductSerializer(product, many=True)
            product_list = serializer.data
            context = {"status": status.HTTP_200_OK, "product_list": product_list}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class WalletWiseSellerListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            seller_wallet = Wallet.objects.filter(user_type="seller")
            print(seller_wallet)
            serializer = WalletSerializer(seller_wallet, many=True)
            seller_wallet = serializer.data
            context = {"status": status.HTTP_200_OK, "seller_wallet": seller_wallet}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class SettlementView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            bills = BillClone.objects.all()
            print(bills)
            serializer = BillCloneSerializer(bills, many=True)
            bills = serializer.data
            context = {"status": status.HTTP_200_OK, "bills": bills}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class FinalSettlementView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            billclone = BillClone.objects.get(id=data.get("id"))
            print(billclone)
            # Send Money from buyer wallet to seller wallet, deducting 95% of the total bill with individual product prices
            seller_wallet = Wallet.objects.get(
                walletuser_id=billclone.bill_item.product.seller.seller.id
            )
            seller_wallet.balance += Decimal(
                (billclone.bill_item.total_price * 95) / 100
            )
            seller_wallet.save()

            # Send Money from buyer wallet to superadmin wallet, 5% of the total bill with individual product prices
            superadmin_wallet = Wallet.objects.get(user_type="superadmin")
            superadmin_wallet.balance += Decimal(
                (billclone.bill_item.total_price * 5) / 100
            )
            superadmin_wallet.save()

            billclone.delete()
            context = {"status": status.HTTP_200_OK, "msg": "Settlement completed"}
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BuyerDashboardView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            items = BillItems.objects.filter(user_id=data.get("user_id"))
            print(items)
            serializer = BuyerDashBoardSerializer(items, many=True)
            buyer_items_list = serializer.data
            context = {
                "status": status.HTTP_200_OK,
                "buyer_items_list": buyer_items_list,
            }
            return Response(
                context,
            )

        except Exception as e:
            # Log the exception or handle it as needed
            print(
                f"An error occurred while retrieving the wallet-wise seller list: {str(e)}"
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)
