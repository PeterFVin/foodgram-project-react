from rest_framework import routers
from django.urls import include, path

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = routers.DefaultRouter()
router_subscr = routers.DefaultRouter()
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"tags", TagViewSet, basename="tags")
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include("djoser.urls")),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
