from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, BuyerSerializer
from buyer.models import Buyer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password


class BuyerSignupApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)
            # if data["password1"] != data["password2"]:
            #     return Response(
            #         {"error": "Passwords do not match"},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                user = serializer.save(password=make_password(data.get("password")))
                phone = data.get(
                    "phone"
                )  # Use get to avoid KeyError if 'phone' is not in data

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







