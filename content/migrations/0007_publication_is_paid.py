# Generated by Django 5.0.2 on 2024-02-26 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0006_dislikes"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="is_paid",
            field=models.BooleanField(default=False, verbose_name="Платная публикация"),
        ),
    ]