from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework import viewsets
from rest_framework import mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from api_yamdb.reviews.models import Review
import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer, \
from .permissions import SuperUserOrAdminOrModeratorOrAuthor
from api.serializers import CategorySerializer, GenreSerializer,\
    TitleSerializer, TitleReadSerializer
from reviews.models import Category, Genre, Title
from reviews.models import User, Title
from .serializers import (CommentSerializer, ReviewSerializer,
                          UserGetTokenSerializers, UserCreateSerializers)
from .token import send_code
from api_yamdb.api.permissions import AuthorAdminModeratorOrReadOnly


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет для модели Category"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет для модели Genre"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title"""

    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleReadSerializer
        return TitleSerializer


class CreateUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Всьюсет для создания обьектов модели User"""

    queryset = User.objects.all()
    serializer_class = UserCreateSerializers
    permission_classes = (permissions.AllowAny,)

    def create_user(self, request):

        serializer = UserCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_code(
            email=user.email,
            confirmation_code=confirmation_code
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для генерации и получения пользователем JWT токена"""

    queryset = User.objects.all()
    serializer_class = UserGetTokenSerializers
    permission_classes = (permissions.AllowAny,)

    def create_JWT(self, request, *args, **kwargs):

        serializer = UserGetTokenSerializers(data=request.data)
        serializer.is_valid(raise_exeption=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
