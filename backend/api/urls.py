from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tags.views import TagViewSet
from recipes.views import RecipeViewSet
from favorites_shop.views import FavoritesView, ShoppingCardView
from users.views import SubscriptionsView
from ingredients.views import IngredientViewSet

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', ShoppingCardView, basename='shopingcards')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'recipes', FavoritesView, basename='favorites')
router.register(r'users', SubscriptionsView, basename='subscriptions')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
