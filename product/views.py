from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializer import *


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewset(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductAttributeViewset(ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class AttributeValueViewset(ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLineViewset(ModelViewSet):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializer