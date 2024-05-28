from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.models import *
from django.contrib.auth.models import User
from product.serializers import SimpleProductLineSerializer


class CRUDCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["cart_id", "productLine_id", "quantity"]
    
    def save(self, **kwargs):
        cart_id = self.validated_data["cart_id"]    # Automatically validating the cart id to get the cart object
        productLine_id = self.validated_data["productLine_id"]  # Automatically validating the sku to get the product line object
        quantity = self.validated_data["quantity"]

        CartItem.objects.create(cart_id=cart_id, productLine_id=productLine_id, quantity=quantity)


class ListCartItemSerializer(serializers.ModelSerializer):
    productLine_id = SimpleProductLineSerializer()
    class Meta:
        model = CartItem
        fields = ["id", "cart_id", "productLine_id", "quantity", "unit_price", "sub_total"]


class AddDestroyCartSerializer(serializers.ModelSerializer):
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
            # Throw a message to create the new user first.
            pass


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = ListCartItemSerializer(many=True)
    total = serializers.SerializerMethodField(method_name="totalPrice")
    class Meta:
        model = Cart
        fields = ["id", "user", "created_at", "updated_at", "items", "total"]

    def totalPrice(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.unit_price for item in items])
        return total
