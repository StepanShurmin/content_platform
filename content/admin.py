from django.contrib import admin

from content.models import Publication


# Register your models here.
@admin.register(Publication)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "publication_date",
        "owner",
    )
