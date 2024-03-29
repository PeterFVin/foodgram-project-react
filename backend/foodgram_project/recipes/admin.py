from django.contrib import admin, messages
from django.contrib.admin import display

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagRecipe,
)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientRecipeInline, TagRecipeInline]
    list_display = ('name', 'id', 'author', 'favorites_added_count')
    readonly_fields = ('favorites_added_count',)
    list_filter = (
        'author',
        'name',
        'tags',
    )
    empty_value_display = 'пусто'

    @display(description='число добавлений в избранное')
    def favorites_added_count(self, obj):
        return obj.favorite.count()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        recipe = form.instance
        if not recipe.tags.exists() or not recipe.ingredients.exists():
            messages.error(request, 'Укажите хотя бы один ингредиент и тег!')
            recipe.delete()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )


@admin.register(IngredientRecipe)
class IngredientRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )


@admin.register(TagRecipe)
class TagRecipe(admin.ModelAdmin):
    list_display = (
        'recipe',
        'tag',
    )
