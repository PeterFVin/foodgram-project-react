from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

# #     class Rolechoices(models.TextChoices):
# #         USER = "user"
# #         MODERATOR = "moderator"
# #         ADMIN = "admin"


    username = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name='имя пользователя',
    #     validators=[
    #         RegexValidator(
    #             regex=r'^[\w.@+-]+$',
    #             message='«Введите допустимое значение».'),
    #     ]
    )
    email = models.EmailField(max_length=100,
                              unique=True,
                              blank=False,
                              verbose_name='e-mail')
    first_name = models.CharField(max_length=30,
                                  blank=False,
                                  verbose_name='имя')
    last_name = models.CharField(max_length=30,
                                 blank=False,
                                 verbose_name='фамилия')
    password = models.CharField(max_length=50,
                                blank=False,
                                verbose_name='пароль')


# #     role = models.CharField(
# #         max_length=10,
#         choices=Rolechoices.choices,
#         default=Rolechoices.USER,
#         verbose_name='пользовательские роли',
#     )
#     confirmation_code = models.CharField(
#         blank=True,
#         max_length=255,
#         verbose_name='код подтверждения',
#     )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'password'
    ]

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        # indexes = [
        #     models.Index(fields=['username'])
        # ]

    def __str__(self):
        return self.username


#     @property
#     def is_admin(self):
#         return (
#             self.role == User.Rolechoices.ADMIN
#             or self.is_superuser
#             or self.is_staff
#         )

#     @property
#     def is_moderator(self):
#         return self.role == User.Rolechoices.MODERATOR

#     @property
#     def is_user(self):
#         return self.role == User.Rolechoices.USER
