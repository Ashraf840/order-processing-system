from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.serializers import ProductLineSerializer
from cart.models import *
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    productLine_id = ProductLineSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "productLine_id", "quantity", "unit_price", "sub_total"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            cart = Cart.objects.get(id=cart_id)
            user = self.context['user']
            # Create order record
            order = Order.objects.create(user=user, cart_id=cart)
            # Get all the cart items of that specific cart
            cartItems = cart.items.all()
            print("cartItem:", cartItems)
            grand_total = 0
            orderItems = []
            for item in cartItems:
                # Check cart item quantity is not bigger than the product stock quantity
                if item.quantity < item.productLine_id.stock.available_unit:
                    grand_total += item.sub_total
                    orderItems.append(
                        OrderItem(
                            productLine_id=item.productLine_id,
                            order_id=order,
                            quantity=item.quantity,
                            unit_price=item.unit_price,
                            sub_total=item.sub_total,
                        )
                    )
            OrderItem.objects.bulk_create(orderItems)
            order.grand_total = grand_total
            order.save()
            # Decrease the product quantity from the stock

            # After creating order items, delete the cart
            # cart.delete()
            return order


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "cart_id", "status", "order_date", "shipping_address", "items", "grand_total"]
