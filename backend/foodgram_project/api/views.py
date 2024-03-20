# from django.db.models import Avg
from datetime import datetime

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# from django.contrib.auth.tokens import default_token_generator
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, response, status, viewsets, mixins
from rest_framework.decorators import action
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import action
# from rest_framework import permissions
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework import filters, mixins, permissions, status, viewsets
# from rest_framework.filters import SearchFilter

from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Tag
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)


# from api.function import send_confirmation_code
# from api.filters import FilterTitle
from api.permissions import AuthorOrReadOnly
# from api.permissions import (
#     IsAdminOrReadOnly,
#     IsSuperUserOrIsAdminOnly,
#     IsReviewAuthorOrReadOnly
# )
# from django.db import IntegrityError


# class APISignup(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.data['username']
#         email = serializer.data['email']

#         try:
#             user, _ = User.objects.get_or_create(
#                 username=username,
#                 email=email
#             )
#         except IntegrityError:
#             return Response(
#                 "ошибка создания пользователя",
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         token = default_token_generator.make_token(user)
#         User.objects.filter(username=username).update(confirmation_code=token)
#         send_confirmation_code(token, email)
#         return Response(
#             {'email': email, 'username': username},
#             status=status.HTTP_200_OK
#         )


# class APIReceiveToken(APIView):
#     def post(self, request):
#         serializer = APIReceiveTokenSerializer(data=request.data)

#         if serializer.is_valid(raise_exception=True):
#             username = serializer.data['username']
#             confirmation_code = serializer.data['confirmation_code']
#             user = get_object_or_404(User, username=username)

#             if default_token_generator.check_token(user, confirmation_code):
#                 token = AccessToken.for_user(user)
#                 return Response(
#                     {"token": str(token)},
#                     status=status.HTTP_200_OK
#                 )
#             message = {
#                 'confirmation_code': f'неверный токен {confirmation_code}'
#             }
#             return Response(message, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [IsSuperUserOrIsAdminOnly]
#     filter_backends = (SearchFilter, )
#     lookup_field = 'username'
#     search_fields = ('username', )
#     http_method_names = ['get', 'post', 'patch', 'delete']

#     @action(
#         detail=False,
#         methods=["get", "patch"],
#         serializer_class=NotAdminSerializer,
#         permission_classes=[IsAuthenticated]
#     )
#     def me(self, request):
#         user = request.user
#         if request.method == 'GET':
#             serializer = self.get_serializer(
#                 user, data=request.data,
#                 partial=True
#             )
#             serializer.is_valid(raise_exception=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         serializer = self.get_serializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)

#         serializer.save(role=user.role, partial=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = (IsReviewAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
#     pagination_class = LimitOffsetPagination

#     def get_queryset(self):
#         review = get_object_or_404(Review,
#                                    id=self.kwargs.get("review_id"),
#                                    title_id=self.kwargs.get("title_id"))
#         return review.comments.all()

#     def perform_create(self, serializer):
#         review = get_object_or_404(Review,
#                                    id=self.kwargs.get("review_id"),
#                                    title_id=self.kwargs.get("title_id"))
#         serializer.save(author=self.request.user, review=review,)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    # permission_classes = (IsReviewAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    # pagination_class = LimitOffsetPagination
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    # permission_classes = (IsReviewAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    # pagination_class = LimitOffsetPagination
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (AuthorOrReadOnly,)
    # pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()

    
    # def get_serializer_class(self, request, queryset):
    #     return RecipeSerializer(queryset, context={'request': request})

    def get_permissions(self):
        if self.action == ('create'):
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self):
        recipe_unit = self.get_object()
        recipe_unit.delete()
        return response.Response('Рецепт успешно удален', status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request.user, pk, request=request)
        else:
            return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk, request=request)
        else:
            return self.delete_recipe(Favorite, request.user, pk)

    def add_recipe(self, model, user, pk, request):
        """Добавление рецепта в избранное или в покупки"""
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return response.Response({'errors': 'Рецепт уже добавлен!'}, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeSerializer(recipe, context={'request': request})
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, pk):
        """Удаление рецепта из избранного или из покупок"""
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response({'errors': 'Рецепт уже удален!'}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        # permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        # shopping_cart = 'Hello\nWorld\n!'
        # response = HttpResponse(shopping_cart, content_type='text/plain')
        # response['Content-Disposition'] = f'attachment; filename=shopping_cart.txt'
        # # shopping_cart = 'Hello\nWorld\n!'
        # # response.writelines(shopping_cart)
        # return response


        
        user = request.user
        # if not user.shopping_cart.exists():
        #     return response.Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = ShoppingCart.objects.filter(
            recipe__shopping_cart__user=request.user.id
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__ingredient_list__amount'))

        # ingredients = IngredientRecipe.objects.filter(
        #     recipe__shopping_cart__user=request.user.id
        # ).values(
        #     'ingredient__name',
        #     'ingredient__measurement_unit'
        # ).annotate(amount=Sum('amount'))

        today = datetime.today()
        shopping_cart = (
            f'Список покупок для Вас на {today:%d-%m-%Y}\n\n'
        )
        shopping_cart += '\n'.join([
            f'- {ingredient["recipe__ingredients__name"]} '
            f'({ingredient["recipe__ingredients__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        shopping_cart += f'\n\nFoodgram. Виноградов Петр. {today:%Y}'

        filename = f'shopping_cart.txt'
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response

    #  ВМЕСТО ПРОСТОГО QUERYSET
    # def get_queryset(self):
    #     title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
    #     return title.reviews.all()

    # def perform_create(self, serializer):
    #     title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
    #     serializer.save(author=self.request.user, title=title)


# class CategoryViewSet(mixins.CreateModelMixin,
#                       mixins.ListModelMixin,
#                       mixins.DestroyModelMixin,
#                       viewsets.GenericViewSet,):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = LimitOffsetPagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
#     filterset_fields = ('name', 'slug')
#     search_fields = ('name', 'slug')
#     lookup_field = 'slug'


# class GenreViewSet(mixins.CreateModelMixin,
#                    mixins.ListModelMixin,
#                    mixins.DestroyModelMixin,
#                    viewsets.GenericViewSet,):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     pagination_class = LimitOffsetPagination
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
#     filterset_fields = ('name', 'slug')
#     search_fields = ('name', 'slug')
#     lookup_field = 'slug'


# class TitleViewSet(viewsets.ModelViewSet):
#     pagination_class = LimitOffsetPagination
#     serializer_class = TitleReadSerializer
#     permission_classes = (IsAdminOrReadOnly,)
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
#     filterset_class = FilterTitle
#     search_fields = ('name', 'year', 'genre__slug', 'category__slug')

#     def get_serializer_class(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return TitleReadSerializer
#         return TitlePostSerializer

#     def get_queryset(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return (Title.objects.select_related('category').all().
#                     annotate(rating=Avg('reviews__score')))
#         return Title.objects.all()
