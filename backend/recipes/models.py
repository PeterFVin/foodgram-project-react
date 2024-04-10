from colorfield.fields import ColorField

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.constants import (
    max_length_common,
    max_cooking_time,
    min_cooking_time,
    max_amount,
    min_amount,
)
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=max_length_common,
                            verbose_name="название")
    measurement_unit = models.CharField(
        max_length=max_length_common,
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
        max_length=max_length_common, unique=True, verbose_name="тег",
    )
    color = ColorField(
        unique=True,
        default="#FF0000",
        verbose_name="цвет",
    )
    slug = models.SlugField(
        max_length=max_length_common, unique=True, verbose_name="slug",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=max_length_common,
                            verbose_name="рецепт")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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
        through="TagRecipe",
        related_name="recipes",
        verbose_name="теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="время приготовления",
        validators=[
            MinValueValidator(
                min_cooking_time,
                message=f"Минимальное значение {min_cooking_time}!",
            ),
            MaxValueValidator(
                max_cooking_time,
                message=f"Максимальное значение {max_cooking_time}!",
            ),
        ],
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
                max_amount,
                message=f"Максимальное значение {max_amount}!",
            ),
            MinValueValidator(
                min_amount,
                message=f"Минимальное значение {min_amount}!",
            ),
        ),
    )

    class Meta:
        verbose_name = "ингредиент в рецепте"
        verbose_name_plural = "ингредиенты в рецепте"
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.recipe} {self.ingredient}"


class TagRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="рецепт",
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="тег")

    class Meta:
        verbose_name = "тег в рецепте"
        verbose_name_plural = "теги в рецепте"
        ordering = ("recipe",)

    def __str__(self):
        return f"{self.recipe} {self.tag}"


class AbstractModel(models.Model):
    """Абстрактная модель для Favorite и ShoppingCart."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )

    class Meta:
        abstract = True


class Favorite(AbstractModel):
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


class ShoppingCart(AbstractModel):
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
