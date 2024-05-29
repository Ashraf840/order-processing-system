from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.serializers import ProductLineSerializer
from cart.models import *
from django.db import transaction
from inventory.models import ProductStock


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
            out_of_stock = []
            for item in cartItems:
                # Check cart item quantity is not bigger than the product stock quantity
                productStock = ProductStock.objects.get(productLine_id=item.productLine_id)
                if item.quantity <= productStock.available_unit:
                    productStock.available_unit -= item.quantity
                    productStock.save()
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
                else:
                    out_of_stock.append({
                        'product': item.productLine_id.product_id.name,
                        'sku': str(item.productLine_id.sku),
                        })
            
            if len(out_of_stock) > 0:
                raise serializers.ValidationError("The following items are out of stock: {}".format(out_of_stock))
            
            OrderItem.objects.bulk_create(orderItems)
            order.grand_total = grand_total
            order.save()

            # After successfully creating order items, delete the cart
            cart.delete()
            
            return order


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ["id", "user", "cart_id", "status", "order_date", "shipping_address", "items", "grand_total"]
