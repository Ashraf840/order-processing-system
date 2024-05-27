from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderItem(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_price = models.FloatField()

ORDER_STATUS_CHOICES = [
    ('P', 'Pending'),
    ('S', 'Successful'),
    ('R', 'Refunded'),
]

class PaymentInformation(models.Model):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES, default='Order Received by Restaurant')
    grand_total = models.FloatField()