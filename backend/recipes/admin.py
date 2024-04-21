from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


class IngredientRecipeInline(admin.TabularInline):

    model = IngredientRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline,)
    list_display = ("name",
                    "id",
                    "author",
                    "favorites_added_count",
                    "ingredients_list",
                    )
    readonly_fields = ("favorites_added_count",)
    list_filter = (
        "author",
        "name",
        "tags",
    )
    empty_value_display = "пусто"

    @display(description="число добавлений в избранное")
    def favorites_added_count(self, obj):
        return obj.favorite.count()

    @display(description="ингредиенты")
    def ingredients_list(self, obj):
        return [ingredient.name for ingredient in obj.ingredients.all()]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "measurement_unit",
    )
    list_filter = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
        "slug",
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "recipe",
    )


@admin.register(IngredientRecipe)
class IngredientRecipe(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "amount",
    )
