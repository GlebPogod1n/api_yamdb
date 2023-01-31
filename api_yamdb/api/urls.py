from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, create,
                       GenreViewSet, UserGetTokenViewSet,
                       TitleViewSet, ReviewViewSet,
                       CommentViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
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
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', create,
         name='signup'),
    path('v1/auth/token/', UserGetTokenViewSet.as_view({'post': 'create'}),
         name='token'),
]
