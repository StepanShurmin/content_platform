from django.conf import settings
from django.contrib.auth.models import AbstractUser

from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    birthday = models.DateField(verbose_name="Дата рождения", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="Город", **NULLABLE)
    phone = models.CharField(unique=True, max_length=100, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    username = models.CharField(unique=True, max_length=100, verbose_name="Логин")
    subscriptions = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=" Подписки", **NULLABLE
    )

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
