from rest_framework import serializers
# from django.core.validators import RegexValidator
# from django.db.models import Avg

from api.utils import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import UserSerializer
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
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'author',
                  'text',
                  'ingredients',
                  'tags',
                  'cooking_time',
                  'is_favorited',
                  'is_in_shopping_cart')
        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    # def current_user(request):
    #     serializer = UserSerializer(request.user)
    #         return Response(serializer.data)

    # def get_author(self, obj):
    #     return dt.datetime.now().year - obj.birth_year
        
    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorite.filter(user=user).exists()
    
    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=user).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
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

    def update(self, instance, validated_data):
        print(validated_data)
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
            )
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(tags)
        
        
        amount_set = IngredientRecipe.objects.filter(
                recipe__id=instance.id)
        print(instance.id)
        amount_set.delete()
        
        IngredientRecipe.objects.bulk_create(
        [IngredientRecipe(
            ingredient=Ingredient.objects.get(id=ingredient_data['id']),
            recipe=instance,
            amount=ingredient_data['amount']
        ) for ingredient_data in ingredients_data]
        )
        instance.save()
        return instance
    
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
