from django.contrib import admin as contribadmin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin

from .models import Subscribe, User


@contribadmin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "username",
        "id",
        "email",
        "first_name",
        "last_name",
        "recipes_count",
        "subscribers_count",
    )
    list_filter = ("email", "username")
    empty_value_display = "пусто"

    @display(description="число рецептов")
    def recipes_count(self, obj):
        return obj.recipes.count()

    @display(description="число подписок")
    def subscribers_count(self, obj):
        return obj.subscriber.count()


@contribadmin.register(Subscribe)
class SubscribeAdmin(contribadmin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
