from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Address


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["uuid", "user"]
        ref_name = 'UserAddressSerializerApp'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]
        ref_name = 'UserSerializerApp'


class UserCreateSerializer_Custom(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["email", "password", "username",]
        ref_name = 'UserCreateSerializer_CustomApp'
