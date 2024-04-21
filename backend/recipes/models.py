from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.constants import (
    MAX_AMOUNT,
    MIN_AMOUNT,
    MAX_COOKING_TIME,
    MIN_COOKING_TIME,
    MAX_LENGTH_COMMON,
)
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_COMMON,
        verbose_name="название")
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_COMMON,
        verbose_name="единица измерения",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"),
                name="unique_ingredient",
            ),
        )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_COMMON,
        unique=True,
        verbose_name="тег",
    )
    color = ColorField(
        unique=True,
        default="#FF0000",
        verbose_name="цвет",
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_COMMON,
        unique=True,
        verbose_name="slug",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_COMMON,
        verbose_name="рецепт")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="создатель рецепта",
    )
    image = models.ImageField(
        verbose_name="изображение",
        upload_to="recipe_images/",
        null=False,
    )
    text = models.TextField(
        null=False,
        verbose_name="описание рецепта",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
        related_name="recipes",
        verbose_name="ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="recipes",
        verbose_name="теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="время приготовления",
        validators=(
            MinValueValidator(
                MIN_COOKING_TIME,
                message=f"Минимальное значение {MIN_COOKING_TIME}!",
            ),
            MaxValueValidator(
                MAX_COOKING_TIME,
                message=f"Максимальное значение {MAX_COOKING_TIME}!",
            ),
        ),
    )

    class Meta:
        ordering = ("name", "author_id")
        verbose_name = "рецепт"
        verbose_name_plural = "рецепты"

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
        related_name="ingredient_list",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="ингредиент",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="количество",
        validators=(
            MaxValueValidator(
                MAX_AMOUNT,
                message=f"Максимальное значение {MAX_AMOUNT}!",
            ),
            MinValueValidator(
                MIN_AMOUNT,
                message=f"Минимальное значение {MIN_AMOUNT}!",
            ),
        ),
    )

    class Meta:
        verbose_name = "ингредиент в рецепте"
        verbose_name_plural = "ингредиенты в рецепте"
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.recipe} {self.ingredient}"


class FavoriteShoppingCartModel(models.Model):
    """Абстрактная модель для Favorite и ShoppingCart."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )

    class Meta:
        abstract = True


class Favorite(FavoriteShoppingCartModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="рецепт",
    )

    class Meta:
        verbose_name = "избранный рецепт"
        verbose_name_plural = "избранные рецепты"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favorite",
            ),
        )

    def __str__(self) -> str:
        return f"Рецепт {self.recipe} в избранном у {self.user}"


class ShoppingCart(FavoriteShoppingCartModel):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="рецепт",
    )

    class Meta:
        verbose_name = "список покупок"
        verbose_name_plural = "списки покупок"
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_shopping_cart",
            ),
        )

    def __str__(self) -> str:
        return f"Рецепт {self.recipe} в списке покупок у {self.user}"
