from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.constants import EMAIL_MAX_LENGTH, USER_COMMON_MAX_LENGTH


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name")

    username = models.CharField(
        max_length=USER_COMMON_MAX_LENGTH,
        unique=True,
        verbose_name="имя пользователя",
        validators=(
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="«Введите допустимое значение».",
            ),
        ),
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name="e-mail",
    )
    first_name = models.CharField(
        max_length=USER_COMMON_MAX_LENGTH,
        verbose_name="имя",
    )
    last_name = models.CharField(
        max_length=USER_COMMON_MAX_LENGTH,
        verbose_name="фамилия",
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name="subscriber",
        verbose_name="подписчик",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="author",
        verbose_name="автор",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"),
                name="unique_subscription",
            ),
            models.CheckConstraint(
                name="users_subscribes_prevent_self_follow",
                check=~models.Q(user=models.F("author")),
            ),
        )
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

    def __str__(self):
        return f"{self.user} подписался на {self.author}"
