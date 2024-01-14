from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Create your views here.


class ProductListAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.filter(is_active=True, quantity__gt=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
