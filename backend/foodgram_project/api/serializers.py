import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
# from django.core.validators import RegexValidator
# from django.db.models import Avg

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe
# from api.validators import validate_name, validate_rating


# class SignupSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         required=True,
#         max_length=150,
#     )
#     username = serializers.CharField(
#         required=True,
#         max_length=150,
#         validators=(
#             validate_name, RegexValidator(
#                 regex=r'^[\w.@+-]+$',
#                 message='«Введите допустимое значение».'),
#         )
#     )


# class APIReceiveTokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True)
#     confirmation_code = serializers.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'confirmation_code')


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'bio',
#             'role'
#         )
#         lookup_field = 'username'


# class NotAdminSerializer(CustomUserSerializer):
#     class Meta(CustomUserSerializer.Meta):
#         read_only_fields = ('role',)


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         slug_field="username",
#         read_only=True,
#         default=serializers.CurrentUserDefault(),
#     )
#     review = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Comment
#         fields = '__all__'




    # author = serializers.SlugRelatedField(
    #     slug_field="username",
    #     read_only=True,
    # )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка 
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    name = serializers.StringRelatedField(
        source='ingredient.name'
    )
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.CharField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'author', 'text', 'ingredients', 'tags', 'cooking_time')

    def create(self, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        print(tags)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        IngredientRecipe.objects.bulk_create(
        [IngredientRecipe(
            ingredient=Ingredient.objects.get(id=ingredient['id']),
            recipe=recipe,
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        )
        return recipe

    # def update(self, instance, validated_data):
    #     if 'ingredients' in self.validated_data:
    #         ingredients_data = validated_data.pop('ingredients')
    #         amount_set = IngredientRecipe.objects.filter(
    #             recipe__id=instance.id)
    #         amount_set.delete()
    #         bulk_create_data = (
    #             IngredientRecipe(
    #                 recipe=Recipe.objects.get(id=ingredient_data['recipe_id']),
    #                 ingredient=ingredient_data['ingredient'],
    #                 amount=ingredient_data['amount'])
    #             for ingredient_data in ingredients_data
    #         )
    #         IngredientRecipe.objects.bulk_create(bulk_create_data)

    #     return super().update(instance, validated_data)
    
    def to_representation(self, obj):
        if 'ingredients' in self.fields:
            self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True
        ).data
        representation['tags'] = TagSerializer(
            obj.tags, many=True
        ).data
        return representation



# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', 'slug')


# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ('name', 'slug')


# class TitleReadSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(many=True, read_only=True)
#     rating = serializers.IntegerField(validators=[validate_rating])


#     class Meta:
#         model = Title
#         fields = ('id',
#                   'name',
#                   'year',
#                   'description',
#                   'category',
#                   'genre',
#                   'rating')


# class TitlePostSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         slug_field='slug', queryset=Category.objects.all()
#     )
#     genre = serializers.SlugRelatedField(
#         slug_field='slug', queryset=Genre.objects.all(),
#         many=True
#     )

#     class Meta:
#         fields = ('id',
#                   'name',
#                   'year',
#                   'description',
#                   'category',
#                   'genre')
#         model = Title
