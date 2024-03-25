from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=32, verbose_name='название')
    measurement_unit = models.CharField(
        max_length=32, verbose_name='единица измерения',
    )

    class Meta:
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='тег')
    color = models.CharField(
        max_length=7, unique=True, default='#FF0000', verbose_name='цвет',
    )
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='рецепт')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='создатель рецепта',
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='recipe_images/',
        default='default.jpg',
        blank=False,
    )
    text = models.TextField(
        blank=False,
        verbose_name='описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        blank=False,
        related_name='recipes',
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        blank=False,
        related_name='recipes',
        verbose_name='теги',
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='время приготовления',
        validators=[MinValueValidator(1, message='Минимальное значение 1!')],
    )

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='ingredient_list',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='ингредиент',
    )
    amount = models.IntegerField(
        verbose_name='количество',
        validators=(
            MinValueValidator(
                1, message='должен быть хотя бы один ингредиент!',
            ),
        ),
    )

    class Meta:
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class TagRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт',
    )
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='тег')

    class Meta:
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} {self.tag}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name_plural = 'избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        )

    def __str__(self) -> str:
        return f'Рецепт {self.recipe} в избранном у {self.user}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name_plural = 'список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )

    def __str__(self) -> str:
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'
