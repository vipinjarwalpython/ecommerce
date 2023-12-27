from rest_framework.response import Response
from seller.api_seller.serializers import CategorySerializer, SellerSerializer
from seller.models import Category, Seller, Product
from rest_framework.decorators import APIView
from django.shortcuts import render, redirect
from rest_framework import status
from django.contrib.auth.models import User
from superadmin.models import Wallet
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class CategoryView(APIView):
    def get(self, request, id=None):
        if id is not None:
            cat = Category.objects.get(id=id)
            serializer = CategorySerializer(cat, many=True)
            return Response(serializer.data)

        cat = Category.objects.all()
        print(cat)
        serializer = CategorySerializer(cat)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            if id is not None:
                cat = Category.objects.get(id=id)
                serializer = CategorySerializer(cat, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(
                    {"error": "Please provide a valid student ID"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        cat = Category.objects.get(id=id)
        serializer = CategorySerializer(cat, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Partial Data Updated"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            if id is not None:
                cat = Category.objects.get(id=id)
                cat.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)


class SellerView(APIView):
    def get(self, request, id=None, format=None):
        if id is not None:
            seller = Seller.objects.get(id=id)
            serializer = SellerSerializer(seller)
            return Response(serializer.data)

        seller = Seller.objects.all()
        serializer = SellerSerializer(seller, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SellerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            if id is not None:
                seller = Seller.objects.get(id=id)
                serializer = SellerSerializer(seller, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(
                    {"error": "Please provide a valid student id "},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None, format=None):
        seller = Seller.objects.get(id=id)
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Partial data updated"})
        return Response(serializer.errors)

    def delete(self, request, id=None, *args, **kwargs):
        try:
            if id is not None:
                seller = Seller.objects.get(id=id)
                seller.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as E:
            return Response(str(E), status=status.HTTP_400_BAD_REQUEST)


class SellerSignupApi(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            seller_firstname = data["seller_firstname"]
            seller_lastname = data["seller_lastname"]
            seller_email = data["seller_email"]
            seller_mobilenumber = data["seller_mobilenumber"]
            seller_username = data["seller_username"]
            seller_password1 = data["seller_password1"]
            seller_password2 = data["seller_password2"]

            if seller_password1 != seller_password2:
                context = {
                    "success": False,
                    "message": "password dost not match",
                    "status": status.HTTP_406_NOT_ACCEPTABLE,
                }
                return Response(context)
            if not User.objects.filter(username=seller_username).exists():
                user = User.objects.create_user(
                    first_name=seller_firstname,
                    last_name=seller_lastname,
                    email=seller_email,
                    username=seller_username,
                    password=seller_password1,
                )

                seller = Seller.objects.create(
                    seller=user,
                    seller_mobilenumber=seller_mobilenumber,
                )

                Wallet.objects.create(walletuser=user, balance=0, user_type="seller")
                user.save()

                refresh = RefreshToken.for_user(seller)
                access_token = str(refresh.access_token)

                context = {
                    "access_token": access_token,
                    "success": True,
                    "message": "Seller created",
                    "status": status.HTTP_201_CREATED,
                }
                return Response(context)
            else:
                context = {
                    "success": False,
                    "message": "password dost not match",
                    "status": status.HTTP_201_CREATED,
                }
                return Response(context)
        except Exception as E:
            return Response(str(E))


class SellerLoginApi(APIView):
    permission_classes = IsAuthenticated

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(data)

            seller_username = data["seller_username"]
            seller_password = data["seller_password"]
            user_seller = User.objects.get(username=seller_username)

            if not Seller.objects.filter(seller_id=user_seller.id).exists():
                context = {
                    "success": False,
                    "message": "Seller not exists",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
                return Response(context)
            user = authenticate(username=seller_username, password=seller_password)
            if user is None:
                context = {
                    "success": False,
                    "message": "Seller not found",
                    "status": status.HTTP_404_NOT_FOUND,
                }
                return Response(context)
            else:
                login(request, user)

                context = {
                    "success": True,
                    "message": "Seller login successfully",
                    "status": status.HTTP_200_OK,
                }
                return Response(context)
        except Exception as E:
            return Response(str(E))


class SellerLogoutApi(APIView):
    def get(self, request):
        try:
            logout(request)
            context = {
                "success": True,
                "message": "Seller logout successfully",
                "status": status.HTTP_200_OK,
            }
            return Response(context)

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"An error occurred during seller logout: {str(e)}")
