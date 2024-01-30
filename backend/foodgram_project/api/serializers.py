from rest_framework import serializers
# from django.core.validators import RegexValidator
# from django.db.models import Avg

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
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


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')


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
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text', 'ingredients', 'tags', 'cooking_time')

    def create(self, validated_data):
        print(validated_data)
        if 'ingredients' not in self.initial_data:
            recipe = Recipe.objects.create(**validated_data)
            return recipe

        else:
            print(validated_data)
            ingredients = validated_data.pop('ingredients')
            print('1')
            ingredient1=Ingredient.objects.get(id=ingredients[0]['id'])
            print(ingredient1.id)
            recipe = Recipe.objects.create(**validated_data)
            IngredientRecipe.objects.bulk_create(
            [IngredientRecipe(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
            )
            print('2')
            # print(ingredients[0])
            # for ingredient in ingredients:
            #     print(ingredient)
            # for ingredient in ingredients:
            #     current_ingredient, status = Ingredient.objects.get_or_create(
            #         **ingredient)
            #     IngredientRecipe.objects.create(
            #         ingredient=current_ingredient, recipe=recipe)
            return recipe
    
    def to_representation(self, obj):
        self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True
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
