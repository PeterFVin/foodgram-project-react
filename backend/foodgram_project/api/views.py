from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import response, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import ListRetrieveViewSet
from api.permissions import AuthorOrReadOnly
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)


class TagViewSet(ListRetrieveViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class IngredientViewSet(ListRetrieveViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == ('create'):
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, pk):
        recipe_unit = self.get_object()
        recipe_unit.delete()
        return response.Response(
            'Рецепт успешно удален',
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(
                ShoppingCart,
                request.user,
                pk,
                request=request,
            )
        else:
            return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk, request=request)
        else:
            return self.delete_recipe(Favorite, request.user, pk)

    def add_recipe(self, model, user, pk, request):
        """Добавление рецепта в избранное или в покупки"""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return response.Response(
                {'errors': 'Рецепт уже добавлен!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not Recipe.objects.filter(id=pk):
            raise ValidationError(
                {'recipes': 'Вы указали несуществующий рецепт!'},
            )
        else:
            recipe = Recipe.objects.get(id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(recipe, context={'request': request})
        represented_data = {
            'id': serializer.data['id'],
            'name': serializer.data['name'],
            'image': serializer.data['image'],
            'cooking_time': serializer.data['cooking_time'],
        }
        return response.Response(
            represented_data,
            status=status.HTTP_201_CREATED,
        )

    def delete_recipe(self, model, user, pk):
        """Удаление рецепта из избранного или из покупок"""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        if Recipe.objects.filter(id=pk).exists():
            return response.Response(
                {'errors': 'Рецепт уже удален!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return response.Response(
                {'errors': 'Такой рецепт не создавался!'},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):

        ingredients = (
            ShoppingCart.objects.filter(
                recipe__shopping_cart__user=request.user.id,
            )
            .values(
                'recipe__ingredients__name',
                'recipe__ingredients__measurement_unit',
            )
            .annotate(amount=Sum('recipe__ingredient_list__amount'))
        )
        today = datetime.today()
        shopping_cart = f'Список покупок для Вас на {today:%d-%m-%Y}\n\n'
        shopping_cart += '\n'.join(
            [
                f'- {ingredient["recipe__ingredients__name"]} '
                f'({ingredient["recipe__ingredients__measurement_unit"]})'
                f' - {ingredient["amount"]}'
                for ingredient in ingredients
            ],
        )
        shopping_cart += f'\n\nFoodgram. Виноградов Петр. {today:%Y}'

        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
