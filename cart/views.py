from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin


class CartViewset(CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    No update of cart will be performed with this API endpoint.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.action in ['create', 'destroy']:
            return AddDestroyCartSerializer
        return CartSerializer


class CartItemViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CartItem.objects.all()
        cart = Cart.objects.get(user=user)
        return CartItem.objects.filter(cart_id=cart)

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return CRUDCartItemSerializer
        return ListCartItemSerializer
