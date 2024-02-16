# from django.core.validators import RegexValidator
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


# NUM_CHARS_TO_PRINT = 15


class Ingredient(models.Model):
    name = models.CharField(max_length=32,
                            verbose_name='название')
    measurement_unit = models.CharField(max_length=32,
                            verbose_name='единица измерения')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32,
                            unique=True,
                            verbose_name='тег')
    color = models.CharField(
        max_length=7,
        unique=True,
        default='#FF0000'
    )
    slug = models.SlugField(unique=True, verbose_name='slug')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100,
                            blank=False,
                            verbose_name='рецепт')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='создатель рецепта',)
    image = models.ImageField(
        'изображение',
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
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        blank=False,
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        blank=False,
        verbose_name='время приготовления')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='recipe',
                                 related_name='ingredient_list',)
    ingredient = models.ForeignKey(Ingredient,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='ingredient')
    amount = models.IntegerField(
        verbose_name='количество',
        validators=(MinValueValidator(
            1, message='должен быть хотя бы один ингредиент!'),
        )
    )

    class Meta:
        ordering = ('recipe',)
        #  ЭТУ ЖЕ ПРОВЕРКУ НА УРОВНЕ СЕРИАЛИЗАТОРА!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'],
                                    name='unique_recipe_ingredient')
        ]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class TagRecipe(models.Model):
    recipe = models.ForeignKey(Recipe,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='recipe')
    tag = models.ForeignKey(Tag,
                                 on_delete=models.DO_NOTHING,
                                 verbose_name='tag')

    class Meta:
        ordering = ('recipe',)

    def __str__(self):
        return f'{self.recipe} {self.tag}'
