from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from api.utils import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        recipe = Tag.objects.create(**validated_data)

        return recipe

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit',
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'author',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )
        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')

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
            [
                IngredientRecipe(
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    recipe=recipe,
                    amount=ingredient['amount'],
                )
                for ingredient in ingredients
            ],
        )
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' not in validated_data:
            raise ValidationError(
                {'ingredients': 'Укажите хотя бы один ингредиент!'},
            )
        if 'tags' not in validated_data:
            raise ValidationError({'ingredients': 'Укажите хотя бы один тег!'})
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time,
        )
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(tags)
        amount_set = IngredientRecipe.objects.filter(recipe__id=instance.id)
        amount_set.delete()
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient=Ingredient.objects.get(
                        id=ingredient_data['id'],
                    ),
                    recipe=instance,
                    amount=ingredient_data['amount'],
                )
                for ingredient_data in ingredients_data
            ],
        )
        instance.save()
        return instance

    def validate_ingredients(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Укажите хотя бы один ингредиент!'},
            )
        ingredients_list = []
        for item in ingredients:
            ingredient = Ingredient.objects.filter(id=item['id'])
            if not ingredient:
                raise ValidationError(
                    {'ingredients': 'Вы указали несуществующий ингредиент!'},
                )
            if item in ingredients_list:
                raise ValidationError(
                    {'ingredients': 'Ингредиенты не могут повторяться!'},
                )
            if int(item['amount']) <= 0:
                raise ValidationError(
                    {'amount': 'Должен быть хотя бы один ингредиент!'},
                )
            ingredients_list.append(item)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({'tags': 'Укажите хотя бы один тег!'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({'tags': 'Теги не могут повторяться!'})
            tags_list.append(tag)
        return value

    def to_representation(self, obj):
        if 'ingredients' in self.fields:
            self.fields.pop('ingredients')
        representation = super().to_representation(obj)
        representation['ingredients'] = IngredientRecipeSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(), many=True,
        ).data
        representation['tags'] = TagSerializer(obj.tags, many=True).data
        return representation
