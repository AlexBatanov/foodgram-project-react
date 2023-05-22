from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, TagViewSet
from users.views import UserViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
v1_router.register(
    r'users',
    UserViewSet,
    basename='users'
)
v1_router.register(
    r'tags',
    TagViewSet,
    basename='tags'
)
print(v1_router.get_urls())
urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]