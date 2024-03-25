from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import CustomPagination
from users.models import Subscribe, User
from users.serializers import (
    SubscribeSerializer,
    CustomUserCreateSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomUserCreateSerializer
        return UserSerializer

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        methods=['POST', 'DELETE'],
    )
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
        if self.request.method == 'POST':
            if Subscribe.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                follow = Subscribe.objects.create(user=user, author=author)
                serializer = SubscribeSerializer(
                    follow, context={'request': request},
                )
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED,
                )
        if self.request.method == 'DELETE':
            if Subscribe.objects.filter(user=user, author=author).exists():
                follow = get_object_or_404(Subscribe, user=user, author=author)
                follow.delete()
                return Response(
                    'Подписка успешно удалена',
                    status=status.HTTP_204_NO_CONTENT,
                )
            else:
                return Response(
                    {'errors': 'Вы не подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        methods=['GET'],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True, context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=[
            'GET',
        ],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        """Функция получения страницы текущего пользователя"""

        if request.method == 'GET':
            serializer = UserSerializer(
                self.request.user, context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"errors": "Только для авторизованных пользователей!"},
            status=status.HTTP_400_BAD_REQUEST,
        )
