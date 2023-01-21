from rest_framework import serializers

from user.models import User, Category, Comment, Genre, Review, Title

class UserCreateSerializers(serializers.ModelSerializer):
    """Серилизатор для создания Usera"""

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )

    def validate(self, data):
        """Проверяем, чтобы пользователь не использовал
        повторные username и email и не присваивал себе имя me"""

        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class UserGetTokenSerializers(serializers.Serializer):
    """Серилизатор при получении токена JWT"""

    username = serializers.CharField(
        max_lenght = 100,
        required=True
    )

    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Серилизатор для объектов модели user"""
    email = serializers.EmailField()


    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio' 
        )

    def valid_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return username


