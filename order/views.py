from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from django.http import JsonResponse
from rest_framework.decorators import action


class OrderViewset(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    # Order record delete using this api is not allowed
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}

    # @action(detail=True, methods=["POST"])
    # def payment(self, request, pk):
    #     return JsonResponse({'msg':'payment successful'})


class PaymentInformationViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentInformationSerializer

    def get_queryset(self):
        user = self.request.user
        o_id = self.kwargs['order_id']
        # return PaymentInformation.objects.all()
        if user.is_staff or user.is_superuser:
            return PaymentInformation.objects.all()
        return PaymentInformation.objects.filter(order_id=o_id)
