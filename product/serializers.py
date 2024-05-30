from rest_framework import serializers
from .models import *


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        ref_name = 'SimpleCategorySerializerApp'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        ref_name = 'CategorySerializerApp'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"
        ref_name = 'BrandSerializerApp'


class SimpleProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]
        ref_name = 'SimpleProductAttributeSerializerApp'


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name"]
        ref_name = 'ProductAttributeSerializerApp'


class SimpleAttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = SimpleProductAttributeSerializer()
    
    class Meta:
        model = AttributeValue
        fields = ["value", "attribute_id"]
        ref_name = 'SimpleAttributeValueSerializerApp'


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_id = ProductAttributeSerializer()
    
    class Meta:
        model = AttributeValue
        fields = ["id", "value", "attribute_id"]
        ref_name = 'AttributeValueSerializerApp'


class UpdatePatchAttributeValueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AttributeValue
        fields = ["id", "value"]
        ref_name = 'UpdatePatchAttributeValueSerializerApp'


class SimpleProductSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    
    class Meta:
        model = Product
        fields = ["name", "category"]
        ref_name = 'SimpleProductSerializerApp'




class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description", "is_active"]
        ref_name = 'UpdateProductSerializerApp'

    
class CRDProductSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()
    
    class Meta:
        model = Product
        fields = ["id", "name", "description", "category"]
        ref_name = 'CRDProductSerializerApp'

    def save(self, **kwargs):
        name = self.validated_data["name"]
        description = self.validated_data["description"]
        category = self.validated_data["category"]
        print("category:", category)
        try:
            category_obj = Category.objects.get(id=category)
            print("category_obj:", category_obj)
            product = Product.objects.create(
                name=name,
                description=description,
                category=category_obj
            )
            print("product:", product)
        except:
            pass


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "is_active", "created_at", "updated_at", "category"]
        ref_name = 'ProductSerializerApp'


class SimpleProductLineSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()
    brand_id = serializers.StringRelatedField()
    attributeValue_id = SimpleAttributeValueSerializer(many=True)
    
    class Meta:
        model = ProductLine
        fields = ["product_id", "brand_id", "attributeValue_id"]
        ref_name = 'SimpleProductLineSerializerApp'


class ProductLineSerializer(serializers.ModelSerializer):
    product_id = SimpleProductSerializer()
    brand_id = serializers.StringRelatedField()
    attributeValue_id = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = ["product_id", "sku", "retail_price", "sale_price", "store_price", "in_stock", "created_at", "updated_at", "brand_id", "attributeValue_id"]
        ref_name = 'ProductLineSerializerApp'
