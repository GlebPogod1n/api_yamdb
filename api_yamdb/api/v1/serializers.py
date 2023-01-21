from django.shortcuts import get_object_or_404
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
        max_lenght=100,
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='id',
        many=False,
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs.get('title_id')
        )
        author = self.context['request'].user
        if Review.objects.filter(title_id=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        many=False,
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
