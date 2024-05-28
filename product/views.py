from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from utils.permissions import mixins


class CategoryViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductAttributeViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class AttributeValueViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer


class ProductViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductLineViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializer