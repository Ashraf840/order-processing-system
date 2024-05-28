from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid
from django.utils.text import slugify

class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, blank=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return f"{self.name} -> {self.parent}"
    
    def save(self, *args, **kwargs):
        # If slug is not provided or is empty, generate it from the name field
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Ensure the slug is unique
        unique_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{self.slug}-{counter}'
            counter += 1
        self.slug = unique_slug

        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
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
    slug = models.SlugField(max_length=120, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Automatically deactive if the product is out of stock from the inventory on every product line.")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        # If slug is not provided or is empty, generate it from the name field
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Ensure the slug is unique
        unique_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{self.slug}-{counter}'
            counter += 1
        self.slug = unique_slug

        super().save(*args, **kwargs)

class ProductLine(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)   # To avoid removing product accidentally from the system, otherwise the entire product line will be deleted from the system.
    sku = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    retail_price = models.FloatField()
    sale_price = models.FloatField()
    store_price = models.FloatField(null=True, blank=True)  # For internal usage
    in_stock = models.BooleanField(default=True, help_text="Automatically deactive if the product line is out of stock.")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.PROTECT, null=True, blank=True)    # To avoid removing the entire product line just by deleting any associated brand.
    attributeValue_id = models.ManyToManyField(AttributeValue, blank=True)

    def __str__(self) -> str:
        return f"{self.product_id}"