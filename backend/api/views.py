from django.db.models import Count, Sum, Prefetch
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    SAFE_METHODS,
)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeGetSerializer,
    RecipeWriteSerializer,
    TagSerializer,
    SubscribeGetSerializer,
    SubscribeWriteSerializer,
    UserSerializer,
)
from api.static_methods import download_shopping_cart_static
from users.models import Subscribe, User
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return (IsAuthenticated(),)
        return super().get_permissions()

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=["post"],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        serializer = SubscribeWriteSerializer(
            author,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.create(user=user, author=author)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def remove_from_shopping_cart(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if Subscribe.objects.filter(user=user, author=author).exists():
            follow = get_object_or_404(Subscribe, user=user, author=author)
            follow.delete()
            return Response(
                "Подписка успешно удалена",
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"errors": "Вы не подписаны на данного пользователя"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        methods=["GET"],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(author__user=user).annotate(
            recipes_count=Count("recipes__author"),
        )
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeGetSerializer(
            pages,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.select_related("author").prefetch_related(
        Prefetch("tags", queryset=Tag.objects.all()),
        Prefetch("ingredients", queryset=Ingredient.objects.all()),
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        return self.add_obj(
            ShoppingCart,
            request.user,
            pk,
            request=request,
        )

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return self.delete_obj(ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return self.add_obj(Favorite, request.user, pk, request=request)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        return self.delete_obj(Favorite, request.user, pk)

    def add_obj(self, model, user, pk, request):
        """Добавление рецепта в избранное или в покупки"""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return response.Response(
                {"errors": "Рецепт уже добавлен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Recipe.objects.filter(id=pk):
            raise ValidationError(
                {"recipes": "Вы указали несуществующий рецепт!"},
            )
        else:
            recipe = Recipe.objects.get(id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeWriteSerializer(recipe,
                                           context={"request": request})
        represented_data = {
            "id": serializer.data["id"],
            "name": serializer.data["name"],
            "image": serializer.data["image"],
            "cooking_time": serializer.data["cooking_time"],
        }
        return response.Response(
            represented_data,
            status=status.HTTP_201_CREATED,
        )

    def delete_obj(self, model, user, pk):
        """Удаление рецепта из избранного или из покупок"""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {"errors": "Удаление невозможно!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(AllowAny,),
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__shopping_cart__user=request.user.id,
            )
            .values(
                "ingredient__name",
                "ingredient__measurement_unit",
            )
            .annotate(amount=Sum("amount"))
            .order_by("ingredient__name")
        )
        return download_shopping_cart_static(ingredients)
