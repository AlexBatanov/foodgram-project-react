from django.contrib import admin

from .models import Tag, Recipe, Ingredient, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag)