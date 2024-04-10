from django.contrib import admin as contribadmin
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
    )
    list_filter = ("email", "username")
    empty_value_display = "пусто"


@contribadmin.register(Subscribe)
class SubscribeAdmin(contribadmin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
