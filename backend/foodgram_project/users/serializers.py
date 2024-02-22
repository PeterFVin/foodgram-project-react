from djoser import serializers

from recipes.models import User


class CustomUserCreateSerializer(serializers.UserCreateSerializer):
    """При создании пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


class UserSerializer(serializers.UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'first_name', 'last_name', 'username', 'password')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation.pop('password')
        return representation
