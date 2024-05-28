from rest_framework import serializers
from .models import *


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class SimpleProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]


class SimpleAttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = SimpleProductAttributeSerializer()
    
    class Meta:
        model = AttributeValue
        fields = ["value", "attribute_id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = ProductAttributeSerializer()
    
    class Meta:
        model = AttributeValue
        fields = ["value", "attribute_id"]


class SimpleProductSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    
    class Meta:
        model = Product
        fields = ["name", "category"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "is_active", "created_at", "updated_at", "category"]


class SimpleProductLineSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()
    brand_id = serializers.StringRelatedField()
    attributeValue_id = SimpleAttributeValueSerializer(many=True)
    
    class Meta:
        model = ProductLine
        fields = ["product_id", "brand_id", "attributeValue_id"]


class ProductLineSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()
    brand_id = serializers.StringRelatedField()
    attributeValue_id = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["product_id", "sku", "retail_price", "sale_price", "store_price", "in_stock", "created_at", "updated_at", "brand_id", "attributeValue_id"]