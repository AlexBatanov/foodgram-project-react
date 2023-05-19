from django.http import HttpResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet
from users.views import TokenLoginViewSet, TokenLogautViewSet, UserViewSet, SetPasswordViewSet

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
    path('users/set_password/', SetPasswordViewSet().as_view()),
    path('', include(v1_router.urls)),
    path('auth/token/login/', TokenLoginViewSet().as_view()),
    path('auth/token/logout/', TokenLogautViewSet().as_view()),
    
]