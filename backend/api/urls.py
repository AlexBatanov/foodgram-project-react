from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, UserViewSet, TokenViewSet

v1_router = DefaultRouter()
v1_router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
v1_router.register(
    r'users',
    UserViewSet,
    basename='recipes'
)
def get_recipe(request):
    return HttpResponse('{"recipe":"sdsd"}')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('signin/', get_recipe),
    path('auth/token/login/', TokenViewSet.as_view())
]