from django.urls import include, path
from rest_framework import routers

from .views import (
    UserGetTokenViewSet, CreateUserViewSet
)

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