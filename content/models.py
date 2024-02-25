from django.db import models
from django.conf import settings

NULLABLE = {"null": True, "blank": True}


class Publication(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
