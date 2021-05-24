from djoser.serializers import UserCreateSerializer

from api.models.user import User


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password')
