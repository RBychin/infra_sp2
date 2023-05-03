from django.urls import include, path
from rest_framework import routers

from api.views import (
    ReviewViewSet,
    CommentViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
)
from users.views import UserViewSet, sign_up, get_token

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename="titles")
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet,
    basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments')
v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token'),
]
