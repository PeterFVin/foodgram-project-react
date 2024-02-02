# from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
# from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models

from colorfield.fields import ColorField


# NUM_CHARS_TO_PRINT = 15


# class User(AbstractUser):

# #     class Rolechoices(models.TextChoices):
# #         USER = "user"
# #         MODERATOR = "moderator"
# #         ADMIN = "admin"

#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         blank=False,
#         verbose_name='имя пользователя',
#     #     validators=[
#     #         RegexValidator(
#     #             regex=r'^[\w.@+-]+$',
#     #             message='«Введите допустимое значение».'),
#     #     ]
#     )
#     email = models.EmailField(unique=True,
#                               max_length=100,
#                               blank=False,
#                               verbose_name='e-mail')
#     first_name = models.CharField(max_length=30,
#                                   blank=True,
#                                   verbose_name='имя')
#     last_name = models.CharField(max_length=30,
#                                  blank=True,
#                                  verbose_name='фамилия')
# #     role = models.CharField(
# #         max_length=10,
#         choices=Rolechoices.choices,
#         default=Rolechoices.USER,
#         verbose_name='пользовательские роли',
#     )
#     confirmation_code = models.CharField(
#         blank=True,
#         max_length=255,
#         verbose_name='код подтверждения',
#     )

#     class Meta:
#         ordering = ['username']
#         indexes = [
#             models.Index(fields=['username'])
#         ]

#     def __str__(self):
#         return self.username

#     @property
#     def is_admin(self):
#         return (
#             self.role == User.Rolechoices.ADMIN
#             or self.is_superuser
#             or self.is_staff
#         )

#     @property
#     def is_moderator(self):
#         return self.role == User.Rolechoices.MODERATOR

#     @property
#     def is_user(self):
#         return self.role == User.Rolechoices.USER


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
                            verbose_name='рецепт')
    # author = models.ForeignKey(User,
    #                            on_delete=models.CASCADE,
    #                            verbose_name='создатель рецепта',)
    image = models.ImageField(
        'изображение',
        upload_to='recipe_images/',
        default='default.jpg'
    )
    text = models.TextField(
        verbose_name='описание рецепта',
    )
    # Преустановленный список, при выборе из него указывается кол-во и ед.изм.
    # ChoiceField
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(verbose_name='время приготовления')

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
