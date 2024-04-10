from rest_framework import routers
from django.urls import include, path

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = routers.DefaultRouter()
router_subscr = routers.DefaultRouter()
router.register(r"ingredients", IngredientViewSet)
router.register(r"recipes", RecipeViewSet)
router.register(r"tags", TagViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path(
        "users/subscriptions/",
        UserViewSet.as_view({"get": "subscriptions"}),
        name="user-subscriptions",
    ),
    path("", include("djoser.urls")),
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
