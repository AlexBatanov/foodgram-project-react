from django.contrib import admin

from .models import Recipe


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
