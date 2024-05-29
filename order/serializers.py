from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer
from product.serializers import ProductLineSerializer
from cart.models import *
from django.db import transaction
from inventory.models import ProductStock
from user.serializers import UserAddressSerializer
from user.models import Address


class OrderItemSerializer(serializers.ModelSerializer):
    productLine_id = ProductLineSerializer()
    class Meta:
        model = OrderItem
        fields = ["id", "productLine_id", "quantity", "unit_price", "sub_total"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    shipping_address = UserAddressSerializer()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            cart = Cart.objects.get(id=cart_id)
            user = self.context['user']
            shipping_address = self.validated_data["shipping_address"]
            # If it's not the customer's default address, the create the address, otherwise fetch the customers default address from the db
            if not shipping_address['is_default_shipping_address']:
                print("shipping address:", shipping_address)
                uadd_serializer = Address.objects.create(
                    user=user,
                    street=shipping_address["street"],
                    city=shipping_address["city"],
                    state=shipping_address["state"],
                    postal_code=shipping_address["postal_code"],
                    country=shipping_address["country"],
                    is_default_shipping_address=shipping_address["is_default_shipping_address"],
                )
            else:
                # filter: user & is_default_shipping_address=true
                pass
            
            # Refined Logic: first check if that specific user has any address in the address table, if no record found then create a new one. But if a record is found which doest
            
            # Create order record
            order = Order.objects.create(user=user, cart_id=cart, shipping_address=uadd_serializer)
            # Get all the cart items of that specific cart
            cartItems = cart.items.all()
            # print("cartItem:", cartItems)
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
            # cart.delete()
            
            return order


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = UserAddressSerializer()
    class Meta:
        model = Order
        fields = ["id", "user", "cart_id", "status", "order_date", "shipping_address", "items", "grand_total"]
