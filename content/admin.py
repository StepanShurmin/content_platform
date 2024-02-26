from django.contrib import admin

from content.models import Publication, Likes, Dislikes


# Register your models here.
@admin.register(Publication)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "publication_date",
        "owner",
    )


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "publication", "is_active")


@admin.register(Dislikes)
class DislikesAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "publication", "is_active")
