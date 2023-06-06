from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through

admin.site.register(RecipeIngredient)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'id', 'author', 'added_in_favorites']
    readonly_fields = ['added_in_favorites']
    list_filter = ['author', 'name', 'tags']

    @admin.display(description='Количество в избранном')
    def added_in_favorites(self, obj):
        return obj.favorites.count()
