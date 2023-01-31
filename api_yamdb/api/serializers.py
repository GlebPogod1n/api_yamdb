from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category"""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre"""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title (для записи)"""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title (для чтения)."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class UserCreateSerializers(serializers.Serializer):
    """Сериализатор для создания Usera"""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    def validate_username(self, data):
        if data.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        return data


class UserGetTokenSerializers(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 'bio'
        )


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
        if not self.context['request'].method == 'POST':
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
