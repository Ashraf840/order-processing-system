from django.db import models
from product.models import ProductLine

class ProductStock(models.Model):
    productLine_id = models.ForeignKey(ProductLine, on_delete=models.CASCADE)
    available_unit = models.IntegerField(default=0)
    threshhold_unit = models.IntegerField(default=10)
    returned_unit = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.productLine_id}"
