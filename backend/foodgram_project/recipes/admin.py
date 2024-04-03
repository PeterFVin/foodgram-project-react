from django import forms
from django.contrib import admin
from django.contrib.admin import display
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    TagRecipe,
)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"

    def clean(self):
        forms_data = self.data
        if (forms_data["ingredient_list-0-ingredient"] != "") and (
            forms_data["tagrecipe_set-0-tag"] != ""
        ):
            return
        else:
            raise ValidationError(_("Укажите хотя бы один ингредиент и тег в рецепте!"))


class IngredientRecipeInline(admin.TabularInline):

    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    form = RecipeAdminForm
    inlines = [IngredientRecipeInline, TagRecipeInline]
    list_display = ("name", "id", "author", "favorites_added_count")
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


@admin.register(TagRecipe)
class TagRecipe(admin.ModelAdmin):
    list_display = (
        "recipe",
        "tag",
    )
