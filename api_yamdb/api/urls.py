from rest_framework import routers
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CreateUserViewSet,
                       GenreViewSet, UserGetTokenViewSet,
                       TitleViewSet)

app_name = 'api'

router = routers.DefaultRouter() 
router.register()


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


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include('api.v1.urls'))
]
