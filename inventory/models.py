from django.db import models
from product.models import ProductLine

class ProductStock(models.Model):
    productLine_id = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    available_unit = models.PositiveBigIntegerField(default=0)
    threshhold_unit = models.PositiveBigIntegerField(default=10)
    returned_unit = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.productLine_id}"
