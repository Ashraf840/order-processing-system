from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class UserCreateSerializer_Custom(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["email", "password", "username",]
