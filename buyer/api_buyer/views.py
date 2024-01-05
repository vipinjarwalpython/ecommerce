from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserSerializer,
    BuyerSerializer,
    BuyerBillingSerializer,
    BuyerWalletSerializer,
    BuyerDashBoardSerializer,
)
from buyer.models import Buyer, CartItem, Product, BillItems, BillClone, BuyersBilling
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from superadmin.models import Wallet
from decimal import Decimal


class BuyerSignupApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)

            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                user = serializer.save(password=make_password(data.get("password")))
                phone = data.get("phone")

                buyer_obj = Buyer.objects.create(
                    buyer=user,
                    phone=phone,
                )
                print(buyer_obj)
                buyer_user = Buyer.objects.get(buyer=user)
                print(buyer_user)
                if buyer_obj is not None:
                    buyer_serializer = BuyerSerializer(buyer_user)

                    print(buyer_serializer.data)

                    login(request, user)
                    print(user.is_authenticated)
                    refresh_token = RefreshToken.for_user(user)
                    token = {
                        "refresh_token": str(refresh_token),
                        "access_token": str(refresh_token.access_token),
                    }
                    context = {
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "message": f"Welcome {user}, you are logged in",
                        "buyer_serializer": buyer_serializer.data,
                        "token": token,
                    }
                    return Response(context)

                else:
                    user.delete()  # Rollback user creation if buyer creation fails
                    return Response(
                        buyer_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


class BuyerLoginApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)

            user = User.objects.filter(username=data["username"])
            print(user)

            if not user.exists():
                context = {
                    "success": False,
                    "message": "Username not found",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }
                return Response(context)

            buyer = authenticate(
                request, username=data["username"], password=data["password"]
            )
            print(buyer)
            if buyer is None:
                context = {
                    "success": False,
                    "message": "Password Incorrect",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }
            else:
                login(request, buyer)
                refresh_token = RefreshToken.for_user(buyer)
                token = {
                    "refresh_token": str(refresh_token),
                    "access_token": str(refresh_token.access_token),
                }
                context = {
                    "success": True,
                    "message": f"Welcome {buyer}, you are logged in",
                    "status": status.HTTP_200_OK,
                    "token": token,
                }
                return Response(context)
        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BuyerLogoutView(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        context = {
            "success": True,
            "message": "Buyer Logout Successfully",
            "status": status.HTTP_200_OK,
        }

        return Response(context)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class CartView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            total_price = []
            user = request.user
            print(user)
            if user.is_authenticated:
                cart_data_list = []
                cart_items = CartItem.objects.filter(user=user)

                for item in cart_items:
                    item.total_price = item.product.price * item.quantity
                    item.save()
                    total_price.append(item.total_price)

                    if item.quantity == 0:
                        cart_items.delete()
                    cart_data = {
                        "product_id": item.product.id,
                        "quantity": item.quantity,
                        "total_price": item.total_price,
                        # "total_products_price": total_products_price,
                    }
                    cart_data_list.append(cart_data)
                total_products_price = sum(total_price)

                print(cart_data_list)
                context = {
                    "cart_items": cart_data_list,
                    "total_products_price": total_products_price,
                }
                return Response(context, status=status.HTTP_200_OK)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            product = Product.objects.get(id=data["id"])
            cart_item, created = CartItem.objects.get_or_create(
                product=product, user=request.user
            )
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
            context = {
                "success": True,
                "message": "Product Added in Cart Successfully",
                "status": status.HTTP_200_OK,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class RemoveToCartView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            # cart_item = CartItem.objects.filter(id=data["id"])
            cart_item = CartItem.objects.get(id=data["id"])
            print(cart_item)

            cart_item.delete()
            context = {
                "success": True,
                "message": "Product removed in Cart Successfully",
                "status": status.HTTP_200_OK,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PlusToCartView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            # cart_item = CartItem.objects.filter(id=data["id"])
            product = Product.objects.get(id=data["id"])
            print(product)
            if product.quantity > 0:
                cart_item, created = CartItem.objects.get_or_create(
                    product=product, user=request.user
                )
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()

                product = Product.objects.get(id=cart_item.product.id)
                product.quantity = product.quantity - 1
                product.save()
                context = {
                    "success": True,
                    "message": "Product plus in Cart Successfully",
                    "status": status.HTTP_200_OK,
                }
                return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class MinusToCartView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            # cart_item = CartItem.objects.filter(id=data["id"])
            cart_item = CartItem.objects.get(id=data["id"])
            print(cart_item)
            if cart_item.quantity > 0:
                cart_item.quantity = cart_item.quantity - 1
                cart_item.save()

                product = Product.objects.get(id=cart_item.product.id)
                product.quantity = product.quantity + 1
                product.save()
                context = {
                    "success": True,
                    "message": "Product minus in Cart Successfully",
                    "status": status.HTTP_200_OK,
                }
                return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BillingView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            user = request.user

            cust_bill = BuyersBilling.objects.create(
                user=user,
                first_name=data["first_name"],
                last_name=data["last_name"],
                address=data["address"],
                city=data["city"],
                postal=data["postal"],
                country=data["country"],
                email=data["email"],
                phone=data["phone"],
                notes=data["notes"],
            )
            cust_bill.save()
            # cuts_bill_get = BuyersBilling.objects.get(user_id=request.user.id)
            # print(cuts_bill_get)
            # bill = BuyerBillingSerializer(cuts_bill_get)

            buy_wallet = Wallet.objects.get(walletuser=user)
            print(buy_wallet)
            if buy_wallet == 0:
                context = {
                    "message": " Your wallet is empty! Please add funds to your wallet",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(context)

            cart_item = CartItem.objects.filter(user_id=user.id)
            print(cart_item)
            total_price = []
            for item in cart_item:
                print(item)
                item.total_price = item.product.price * item.quantity
                item.save()

                total_price.append(item.total_price)

            total_product_price = sum(total_price)
            print(total_price)
            print(total_product_price)

            context = {
                "success": True,
                "message": "bill created Successfully",
                "status": status.HTTP_200_OK,
                # "bill": bill.data,
                "total_product_price": total_product_price,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BillConfirmView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            print(user)
            cart_item = CartItem.objects.filter(user_id=user.id)
            print(cart_item)
            cust_bill = BuyersBilling.objects.filter(user=user)
            print(cust_bill)
            last_bill = cust_bill[len(cust_bill) - 1]
            print(last_bill)

            total_price = []
            for item in cart_item:
                item.total_price = item.product.price * item.quantity
                item.save()

                total_price.append(item.total_price)

            total_product_price = sum(total_price)

            buy_wallet = Wallet.objects.get(walletuser=user)
            if buy_wallet.balance < total_product_price:
                context = {
                    "message": " Your wallet ammount is less than the total amount. Please add funds to your wallet.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(context)

            cuts_bill_get = BuyersBilling.objects.get(user_id=request.user.id)
            print(cuts_bill_get)
            bill = BuyerBillingSerializer(cuts_bill_get)

            context = {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "bill confirmation ",
                "bill": bill.data,
                "total_product_price": total_product_price,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ThankyouView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            total_ammount = 0
            user = request.user
            cart_item = CartItem.objects.filter(user_id=user.id)
            print(cart_item)

            for item in cart_item:
                final_bill = BillItems.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    user=item.user,
                    total_price=item.total_price,
                )
                final_bill.save()

                total_ammount = total_ammount + item.product.price

                product = Product.objects.get(name=item.product)

                if product.quantity > 0:
                    product.quantity = product.quantity - item.quantity
                    product.save()
                else:
                    context = {
                        "message": " Product Quanity is less than 0",
                        "status": status.HTTP_400_BAD_REQUEST,
                    }
                    return Response(context)

                billclone = BillClone.objects.create(bill_item=final_bill)
                billclone.save()

            buy_wallet = Wallet.objects.get(walletuser=user)
            if buy_wallet.balance == 0:
                context = {
                    "message": "Your wallet has no balance.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(context)

            remain_ammount = buy_wallet.balance - total_ammount

            buy_wallet.balance = remain_ammount
            buy_wallet.save()

            cart_item.delete()
            context = {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": f"Thank You {user}, Visit Again ",
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AddFundView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            if data is not None:
                ammount = Decimal(data["ammount"])
                buyer_wallet = Wallet.objects.get(walletuser=request.user)

                buyer_wallet.balance = buyer_wallet.balance + ammount
                buyer_wallet.save()
                context = {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": f"Ammount: Rs.{ammount} has Added and your wallet balance is Rs.{buyer_wallet.balance}",
                }
                return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class WithdrawFundView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            if data is not None:
                ammount = Decimal(data["ammount"])
                buyer_wallet = Wallet.objects.get(walletuser=request.user)
                if buyer_wallet.balance == 0:
                    context = {
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Your wallet has no balance.",
                    }
                    return Response(context)

                buyer_wallet.balance = buyer_wallet.balance - ammount
                buyer_wallet.save()
                context = {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": f"Ammount : Rs. {ammount} has withdraw and your remaining balance is {buyer_wallet.balance}",
                }
                return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BuyerWalletView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user

            buy_wallet = Wallet.objects.get(walletuser=user)
            buyer_wallet = BuyerWalletSerializer(buy_wallet)
            context = {
                "success": True,
                "Status": status.HTTP_200_OK,
                "wallet": buyer_wallet.data,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class BuyerDashBoardView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            item_list = []
            items = BillItems.objects.filter(user=user)
            serializer = BuyerDashBoardSerializer(items, many=True)
            buyer_items = serializer.data
            context = {
                "success": True,
                "Status": status.HTTP_200_OK,
                "buyer_items": buyer_items,
            }
            return Response(context)

        except Exception as E:
            return Response({"error": str(E)}, status=status.HTTP_400_BAD_REQUEST)
