from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdminOrReadOnly
from api.serializers import CategorySerializer, GenreSerializer, \
    TitleSerializer, TitleReadSerializer
from user.models import Category, Genre, Title


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
