from django.db import models
from django.contrib.auth.models import User
from product.models import ProductLine
from cart.models import Cart
import uuid
from user.models import Address

ORDER_STATUS_CHOICES = [
    ('P', 'Pending'),
    ('S', 'Successful'),
    ('R', 'Refunded'),
    ('F', 'Failed'),
    ('C', 'Cancelled'),
]

class Order(models.Model):
    # Even after removing the foreign keys records from parent table, the order will be persistent for further data analytics.
    # uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Pending')
    order_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    grand_total = models.FloatField(blank=True)

    def __str__(self) -> str:
        return f"order-{self.user}-{self.order_date}"
        return f"order-{self.user}-{self.created_at}-{self.uuid}"

class OrderItem(models.Model):
    # Doesn't require "created_at" or "updated_at" since the order items will be generated at once. 
    productLine_id = models.ForeignKey(ProductLine, on_delete=models.SET_NULL, null=True)   # For further analytics
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)   # Manually delete all the order items before deleteing the order
    quantity = models.PositiveBigIntegerField()
    unit_price = models.FloatField(blank=True)
    sub_total = models.FloatField(blank=True)

    def __str__(self) -> str:
        return f"order-{self.order_id.user}-{self.productLine_id.product_id}"
    
    def save(self, *args, **kwargs):
        # Automatically set the product unit price
        if not self.unit_price:
            self.unit_price = self.productLine_id.sale_price
        
        # Automatically set the sub total price
        if not self.sub_total:
            self.sub_total = self.quantity * self.productLine_id.sale_price
        super().save(*args, **kwargs)

class PaymentInformation(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    amount = models.FloatField(blank=True)  # amount = Order.grand_total
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"payment-{self.order_id}-{self.payment_date}"