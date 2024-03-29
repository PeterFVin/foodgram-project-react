from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.views import UserViewSet


router = routers.DefaultRouter()
router_subscr = routers.DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'api/users/subscriptions/',
        UserViewSet.as_view({'get': 'subscriptions'}),
        name='user-subscriptions',
    ),
    path('api/', include('djoser.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
