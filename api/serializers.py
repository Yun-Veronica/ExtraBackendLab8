from rest_framework import serializers
from .models import Product, Category, User, Order


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    user = UserSerializer
    class Meta:
        model = Order
        fields = '__all__'
