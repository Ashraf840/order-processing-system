from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "cart_id", "status", "order_date", "shipping_address", "grand_total"]
