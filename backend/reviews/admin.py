from django.contrib import admin

from .models import Tag, Recipe, Ingredient, RecipeIngredient, IsFaworite, ShoppingCard
from users.models import Subscription


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass

@admin.register(IsFaworite)
class IsFaworiteAdmin(admin.ModelAdmin):
    pass

@admin.register(ShoppingCard)
class ShoppingCardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag)