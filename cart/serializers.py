from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.models import *
from django.contrib.auth.models import User
from product.serializers import SimpleProductLineSerializer
from inventory.models import ProductStock


class CRUDCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["cart_id", "productLine_id", "quantity"]
        ref_name = 'CRUDCartItemSerializerApp'
    
    def validate(self, attrs):
        # Check if the product quantity is avaiable in the stock
        cart_id = attrs.get("cart_id")
        productLine_id = attrs.get("productLine_id")
        quantity = attrs.get("quantity")
        previous_cart_unit = 0

        # Get the previous unit if exist
        try:
            cartItem = CartItem.objects.get(cart_id=cart_id, productLine_id=productLine_id)
            previous_cart_unit += cartItem.quantity
        except:
            pass
        
        product_stock = ProductStock.objects.get(productLine_id=productLine_id)
        
        if self.context['request'].method == "POST":
            if quantity > product_stock.available_unit:
                raise serializers.ValidationError("Product stock is not available")
            quantity += previous_cart_unit
        
        if self.context['request'].method == "PUT":
            if quantity > product_stock.available_unit:
                raise serializers.ValidationError("Product stock is not available")
            quantity = previous_cart_unit

        
        return super().validate(attrs)
    
    def save(self, **kwargs):
        cart_id = self.validated_data["cart_id"]    # Automatically validating the cart id to get the cart object
        productLine_id = self.validated_data["productLine_id"]  # Automatically validating the sku to get the product line object
        quantity = self.validated_data["quantity"]

        # Check if the product line already exist, then only increase the quantity
        try:
            cartItem = CartItem.objects.get(cart_id=cart_id, productLine_id=productLine_id)
            # print("self.context['request'].method:", self.context['request'].method)
            if self.context['request'].method == 'PATCH' or self.context['request'].method == 'PUT':
                cartItem.quantity = quantity
            else:
                cartItem.quantity += quantity
            cartItem.save()
        except:
            cartItem = CartItem.objects.create(cart_id=cart_id, productLine_id=productLine_id, quantity=quantity)


class ListCartItemSerializer(serializers.ModelSerializer):
    productLine_id = SimpleProductLineSerializer()
    class Meta:
        model = CartItem
        fields = ["id", "cart_id", "productLine_id", "quantity", "unit_price", "sub_total"]
        ref_name = 'ListCartItemSerializerApp'


class AddDestroyCartSerializer(serializers.ModelSerializer):
    user = serializers.EmailField()
    class Meta:
        model = Cart
        fields = ["user"]
        ref_name = 'AddDestroyCartSerializerApp'
    
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
        ref_name = 'CartSerializerApp'

    def totalPrice(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.unit_price for item in items])
        return total
