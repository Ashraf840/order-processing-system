from django.shortcuts import render
from .models import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from utils.permissions import mixins
from rest_framework.response import Response
from rest_framework import status


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

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdatePatchAttributeValueSerializer
        return AttributeValueSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        value = data.get('value')
        
        try:
            attribute_name = data.get('attribute_id').get('name')
        except:
            attribute_name = data.get('attribute_id.name')

        try:
            product_attribute = ProductAttribute.objects.get(name=attribute_name)

            instance = AttributeValue.objects.create(
                value=value,
                attribute_id=product_attribute,
            )

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            data = {'error': "Product attribute is not found! Please create the new product attribute first."}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class ProductViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductSerializer
        if (self.request.method == "PUT") or (self.request.method == "PATCH"):
            return UpdateProductSerializer
        return CRDProductSerializer


class ProductLineViewset(mixins.StaffOrAdminViewSetMixin, ModelViewSet):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializer