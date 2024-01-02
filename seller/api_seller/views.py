from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, SellerSerializer
from seller.models import Seller
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password


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
