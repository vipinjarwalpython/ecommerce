from buyer.models import Buyer, CartItem
from buyer.api_buyer.serializers import BuyerSerializer, CartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from superadmin.models import Wallet
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


# from rest_framework.permissions import IsAuthenticated


class BuyerSignupApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            first_name = data["first_name"]
            last_name = data["last_name"]
            username = data["username"]
            email = data["email"]
            phone = data["phone"]
            password1 = data["password1"]
            password2 = data["password2"]

            print(password1, password2)

            if password1 != password2:
                context = {
                    "success": False,
                    "message": "Password does not match.",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }

                return Response(context)

            if not User.objects.filter(username=username).exists():
                buyer = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )

                Buyer.objects.create(
                    buyer=buyer,
                    phone=phone,
                )

                Wallet.objects.create(walletuser=buyer, balance=0, user_type="buyer")
                buyer.save()

                refresh = RefreshToken.for_user(buyer)
                access_token = str(refresh.access_token)
                context = {
                    "access_token": access_token,
                    "success": True,
                    "message": "Buyer created",
                    "status": status.HTTP_201_CREATED,
                }

                return Response(context)

            else:
                context = {
                    "success": False,
                    "message": "User already Exists",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }

                return Response(context)

        except Exception as E:
            return Response(str(E))


class BuyerLoginApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            if request.method == "GET":
                username = data["username"]
                password = data["password"]

            if not User.objects.filter(username=username).exists():
                context = {
                    "success": False,
                    "message": "Username not found",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }

                return Response(context)

            buyer_user = User.objects.get(username=username)

            if not Buyer.objects.filter(buyer_id=buyer_user.id).exists():
                context = {
                    "success": False,
                    "message": "Username not found",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }

                return Response(context)

            buyer = authenticate(request, username=username, password=password)

            if buyer is None:
                context = {
                    "success": False,
                    "message": "Username and password is incorrect",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }

                return Response(context)
            else:
                login(request, buyer)
                context = {
                    "success": True,
                    "message": "User Logged in",
                    "status": status.HTTP_200_OK,
                }

                return Response(context)

        except Exception as E:
            return Response(str(E))


# class BuyerLogoutApi(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             logout(request)
#             context = {
#                 "success": True,
#                 "message": "User Logged out",
#                 "status": status.HTTP_200_OK,
#             }
#             return Response(context)

#         except Exception as E:
#             return Response(str(E))


class BuyerApi(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, id=None):
        try:
            if id is not None:
                buyer = Buyer.objects.get(pk=id)
                serialzer = BuyerSerializer(buyer)
                return Response(serialzer.data)

            buyer = Buyer.objects.all()
            serialzer = BuyerSerializer(buyer, many=True)
            return Response(serialzer.data)

        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            buyer = Buyer.objects.get(id=id)
            buyer.delete()
            return Response({"msg": "Data Deleted"}, status=status.HTTP_200_OK)

        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)


class CartItemApi(APIView):
    permission_classes = (IsAuthenticated,)

    def cartitems(self, request, *args, **kwargs):
        try:
            total_price = []
            user = request.user
            if not user.is_authenticated:
                return Response(
                    {"error": "User not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                cart_items = CartItem.objects.filter(user=request.user)

                for item in cart_items:
                    item.total_price = item.product.price * item.quantity
                    item.save()

                    total_price.append(item.total_price)

                    if item.quantity == 0:
                        cart_items.delete()

                total_product_price = sum(total_price)

                serializer = CartItemSerializer(cart_items, many=True)

                return Response(
                    {
                        "cart_items": serializer.data,
                        "total_product_price": total_product_price,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
