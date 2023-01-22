from rest_framework import routers
from django.urls import include, path

from api.views import (CategoryViewSet, CreateUserViewSet,
                       GenreViewSet, UserGetTokenViewSet,
                       TitleViewSet, ReviewViewSet,
                       CommentViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


auth_urls = [
    path(
        'signup/',
        CreateUserViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        UserGetTokenViewSet.as_view({'post': 'create'}),
        name='token'
    )
]

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('v1/', include('api.urls'))
]
