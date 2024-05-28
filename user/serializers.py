from djoser.serializers import UserCreateSerializer

class UserCreateSerializer_Custom(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ["email", "password", "username",]
