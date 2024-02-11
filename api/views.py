from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import Product, Category, User, Order
from .serializers import ProductSerializer, CategorySerializer, UserSerializer, OrderSerializer


# Create your views here.


class ProductListAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.filter(is_active=True, quantity__gt=0)
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, product_id):
        try:
            products = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(products)
        except Product.DoesNotExist():
            return Response({"error": "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductBuyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        if user.is_authenticated:
            try:
                user = User.object.get(pk=user.id)
                product = Product.object.get(pk=product_id)
            except (Product.DoesNotExist, User.DoesNotExist):
                return Response({"error": "Product or User does not exist"}, status=status.HTTP_404_NOT_FOUND)

            order_data = {
                'product': product,
                'user': user,
                'date': datetime.now()
            }
            serializer = OrderSerializer(order_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryListView(APIView):
    def get(self, request, format=None):
        categories = Category.objects.filter()
        serializer = ProductSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryProductListView(APIView):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)
        product = Product.objects.filter(category=category)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserSerializer
    # def post(self, request):
    #     if self.serializer_class.is_valid:
    #         return Response (status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_404_NOT_FOUND)

class UserOrderListView(APIView):
    def post(self, request, user_id):
        permission_classes = [IsAuthenticated]

        if request.user.is_authenticated and request.user.id == user_id:
            try:
                user = User.objects.get(pk=user_id)
                orders = Order.objects.filter(user=user)
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist or Order.DoesNotExist:
                return Response({"error": "Orders for such users does not exist"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "You don't have permission to access this resource."},
                        status=status.HTTP_403_FORBIDDEN)
