from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.models import Subscribe


User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "first_name",
            "last_name",
            "username",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return (
            self.context["request"].user.is_authenticated
            and obj.subscriber.filter(user=user, author=obj).exists()
        )


class RecipeSubscribeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscribeGetSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.user,
            author=obj.author,
        ).exists()

    def get_recipes(self, obj):
        request = self.context["request"]
        limit = request.GET.get("recipes_limit")
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            try:
                int(limit)
                queryset = queryset[: int(limit)]
            except BaseException:
                TypeError("Необходимо значение типа Integer.")
        return RecipeSubscribeSerializer(queryset, many=True).data


class SubscribeWriteSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source="author.email")
    username = serializers.ReadOnlyField(source="author.username")
    first_name = serializers.ReadOnlyField(source="author.first_name")
    last_name = serializers.ReadOnlyField(source="author.last_name")
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Subscribe
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def validate(self, data):
        author = self.instance
        user = self.context["request"].user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError("Подписка уже оформлена.")
        if user == author:
            raise serializers.ValidationError(
                "Вы не можете подписаться на себя!",
            )
        return data

    def to_representation(self, instance):
        request = self.context["request"]
        context = {"request": request}
        return SubscribeGetSerializer(instance, context=context).data


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientRecipeGetSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(source="ingredient_id", read_only=True)
    name = serializers.StringRelatedField(source="ingredient.name")
    measurement_unit = serializers.StringRelatedField(
        source="ingredient.measurement_unit",
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")
        read_only_fields = ("id", "name", "measurement_unit")


class RecipeGetSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeGetSerializer(
        source="ingredient", many=True, required=True,
    )
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "author",
            "text",
            "ingredients",
            "tags",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
        )
        read_only_fields = ("author", "is_favorited", "is_in_shopping_cart")

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        return (
            self.context["request"].user.is_authenticated
            and obj.favorite.filter(user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        return (
            self.context["request"].user.is_authenticated
            and obj.shopping_cart.filter(user=user).exists()
        )

    def to_representation(self, obj):
        if "ingredients" in self.fields:
            self.fields.pop("ingredients")
        representation = super().to_representation(obj)
        representation["ingredients"] = IngredientRecipeGetSerializer(
            IngredientRecipe.objects.filter(recipe=obj).all(),
            many=True,
        ).data
        representation["tags"] = TagSerializer(obj.tags, many=True).data
        return representation


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class RecipeWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeWriteSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True,
    )
    image = Base64ImageField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "author",
            "text",
            "ingredients",
            "tags",
            "cooking_time",
        )
        read_only_fields = ("author",)

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.shopping_cart.filter(user=user).exists()

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(
            **validated_data, author=self.context["request"].user,
        )
        recipe.tags.set(tags)
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=(self.initial_data["ingredients"]
                                   [number]["id"]),
                    recipe=recipe,
                    amount=ingredient["amount"],
                )
                for number, ingredient in enumerate(ingredients)
            ],
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        amount_set = IngredientRecipe.objects.filter(recipe__id=instance.id)
        amount_set.delete()
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=(self.initial_data["ingredients"]
                                   [number]["id"]),
                    recipe=instance,
                    amount=ingredient_data["amount"],
                )
                for number, ingredient_data in enumerate(ingredients_data)
            ],
        )
        return super().update(instance, validated_data)

    def validate(self, value):
        ingredients = value
        if not ingredients:
            raise ValidationError(
                {"ingredients": "Укажите хотя бы один ингредиент!"},
            )
        ingredients_list = []
        for item in self.initial_data["ingredients"]:
            ingredient = Ingredient.objects.filter(id=item["id"])
            if not ingredient:
                raise ValidationError(
                    {"ingredients": "Это несуществующий ингредиент!"},
                )
            if item["id"] in ingredients_list:
                raise serializers.ValidationError(
                    "Нельзя указывать одинаковые ингредиенты.",
                )
            ingredients_list.append(item["id"])
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError({"tags": "Укажите хотя бы один тег!"})
        tags_set = set(tags)
        if len(tags) != len(tags_set):
            raise ValidationError({"tags": "Теги не могут повторяться!"})
        return value

    def to_representation(self, instance):
        request = self.context["request"]
        context = {"request": request}
        return RecipeGetSerializer(instance, context=context).data
