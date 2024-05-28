from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.models import *
from django.contrib.auth.models import User


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class SimpleProductSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    class Meta:
        model = Product
        fields = ["name", "category"]


class SimpleProductAttribute(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]


class SimpleAttributeValue(serializers.ModelSerializer):
    attribute_id = SimpleProductAttribute()
    class Meta:
        model = AttributeValue
        fields = ["value", "attribute_id"]


class SimpleProductLineSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()
    brand_id = serializers.StringRelatedField()
    attributeValue_id = SimpleAttributeValue(many=True)
    class Meta:
        model = ProductLine
        fields = ["product_id", "brand_id", "attributeValue_id"]


class CartItemSerializer(serializers.ModelSerializer):
    productLine_id = SimpleProductLineSerializer()
    class Meta:
        model = CartItem
        fields = ["id", "cart_id", "productLine_id", "quantity", "unit_price", "sub_total"]


class AddUpdateCartSerializer(serializers.ModelSerializer):
    user = serializers.EmailField()
    class Meta:
        model = Cart
        fields = ["user"]
    
    def save(self, **kwargs):
        user_email = self.validated_data["user"]
        try:
            user = User.objects.get(email=user_email)
            if not Cart.objects.filter(user=user).exists():
                Cart.objects.create(user=user)
        except:
            pass


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = CartItemSerializer(many=True)
    total = serializers.SerializerMethodField(method_name="totalPrice")
    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "items", "total"]

    def totalPrice(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.unit_price for item in items])
        return total
