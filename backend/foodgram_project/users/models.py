from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name="имя пользователя",
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="«Введите допустимое значение».",
            ),
        ],
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name="e-mail",
    )
    first_name = models.CharField(
        max_length=30,
        blank=False,
        verbose_name="имя",
    )
    last_name = models.CharField(
        max_length=30,
        blank=False,
        verbose_name="фамилия",
    )
    password = models.CharField(
        max_length=300,
        blank=False,
        verbose_name="пароль",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    class Meta:
        ordering = ["username"]
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
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_subscription",
            ),
        ]
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

    def __str__(self):
        return f"{self.user} подписался на {self.author}"
