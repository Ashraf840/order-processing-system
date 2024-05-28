from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from rest_framework import permissions


class IsStaffOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # General user is prohibited
        if not user.is_authenticated:
            return False
                
        # Allow staff or admin users only
        if user.is_staff or user.is_superuser:
            return True
        return False


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsStaffOrAdmin()]
        return [permissions.AllowAny()]


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