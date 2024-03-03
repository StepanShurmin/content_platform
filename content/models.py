from django.db import models
from django.conf import settings

NULLABLE = {"null": True, "blank": True}


class Publication(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержание")
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        **NULLABLE,
    )
    is_paid = models.BooleanField(default=False, verbose_name="Платная публикация")
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"


class Likes(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, verbose_name="Запись"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Лайкнул"
    )
    is_active = models.BooleanField(default=False, verbose_name="Лайк")

    def __str__(self):
        return f"Лайк для публикации {self.publication} от {self.user}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Dislikes(models.Model):
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, verbose_name="Запись"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Дизлайкнул"
    )
    is_active = models.BooleanField(default=False, verbose_name="Дизлайк")

    def __str__(self):
        return f"Дизлайк для публикации {self.publication} от {self.user}"

    class Meta:
        verbose_name = "Дизлайк"
        verbose_name_plural = "Дизлайки"
