from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class CartViewset(ModelViewSet):
    # queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Cart.objects.all()
        return Cart.objects.filter(user=user)


class CartItemViewset(ModelViewSet):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CartItem.objects.all()
        cart = Cart.objects.get(user=user)
        return CartItem.objects.filter(cart_id=cart)
