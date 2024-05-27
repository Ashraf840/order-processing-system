from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name

class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute_id = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.attribute_id} - {self.value}"

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Automatically deactive if the product is out of stock from the inventory on every product line.")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class ProductLine(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    sku = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    retail_price = models.FloatField()
    sale_price = models.FloatField()
    in_stock = models.BooleanField(default=True, help_text="Automatically deactive if the product line is out of stock.")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)
    attrubuteValue_id = models.ManyToManyField(AttributeValue, blank=True)

    def __str__(self) -> str:
        return f"{self.product_id}"