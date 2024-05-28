from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = ProductAttributeSerializer()
    
    class Meta:
        model = AttributeValue
        fields = ["value", "attribute_id"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "is_active", "created_at", "updated_at", "category"]


class ProductLineSerializer(serializers.ModelSerializer):
    brand_id = serializers.StringRelatedField()
    attributeValue_id = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["product_id", "sku", "retail_price", "sale_price", "store_price", "in_stock", "created_at", "updated_at", "brand_id", "attributeValue_id"]

