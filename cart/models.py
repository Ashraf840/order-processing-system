from django.db import models
from django.contrib.auth.models import User
from product.models import ProductLine

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    # If the user is removed, although the cart will be in the system from future analytics
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"cart-{self.user}-{self.created_at}"

class CartItem(models.Model):
    productLine_id = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")   # Used 'related_name', because we can make the reverse query (From cart model to this model. ie. Cart.items.all())
    quantity = models.PositiveBigIntegerField()
    unit_price = models.FloatField(blank=True)
    sub_total = models.FloatField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"cart-{self.cart_id.user}-{self.productLine_id.product_id}"
    
    def save(self, *args, **kwargs):
        # Automatically set the unit price
        if not self.unit_price:
            self.unit_price = self.productLine_id.sale_price
        
        # Automatically set the sub total price
        if not self.sub_total:
            self.sub_total = self.quantity * self.productLine_id.sale_price
        super().save(*args, **kwargs)