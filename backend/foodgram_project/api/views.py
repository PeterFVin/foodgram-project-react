# from django.db.models import Avg
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.tokens import default_token_generator
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import (
#     IsAuthenticated,
#     IsAuthenticatedOrReadOnly
# )
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import action
# from rest_framework import permissions
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework import filters, mixins, permissions, status, viewsets
# from rest_framework.filters import SearchFilter

# from reviews.models import Category, Genre, Review, Title, User
from recipes.models import Ingredient, Recipe, Tag
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)

# CategorySerializer,
# CommentSerializer,
# CustomUserSerializer,
# GenreSerializer,
# ReviewSerializer,
# TitlePostSerializer,
# TitleReadSerializer,
# APIReceiveTokenSerializer,
# SignupSerializer,
# NotAdminSerializer

# from api.function import send_confirmation_code
# from api.filters import FilterTitle
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
    # permission_classes = (IsReviewAuthorOrReadOnly, IsAuthenticatedOrReadOnly)
    # pagination_class = LimitOffsetPagination
    queryset = Recipe.objects.all()

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
