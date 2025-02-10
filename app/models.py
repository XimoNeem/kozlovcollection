from django.db import models
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Artist(models.Model):
    name = models.CharField("Имя", max_length=255)
    description = models.TextField("Описание")
    birth_year = models.IntegerField("Год рождения", blank=True, null=True)
    death_year = models.IntegerField("Год смерти", blank=True, null=True)
    photo = models.ImageField("Фото", upload_to="artists/", blank=True, null=True)
    photoAuthor = models.CharField("Автор фото", max_length=255)
    textAuthor = models.CharField("Автор текста", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_image(self):
        if self.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.photo.url)
        return "Нет изображения"
    
    preview_image.short_description = "Превью"

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField("Название", max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artworks")
    year = models.IntegerField("Год создания", blank=True, null=True)
    images = models.JSONField("Изображения", blank=True, null=True)  # Хранит список URL-ов изображений
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_images(self):
        if self.images and isinstance(self.images, list) and len(self.images) > 0:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.images[0])
        return "Нет изображений"

    preview_images.short_description = "Превью"

    def __str__(self):
        return self.title


class PressMention(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    link = models.URLField("Ссылка")
    image = models.ImageField("Изображение", upload_to="press_mentions/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.image.url)
        return "Нет изображения"

    preview_image.short_description = "Превью"

    def __str__(self):
        return self.title


class Route(models.Model):
    name = models.CharField("Название маршрута", max_length=255, default="Маршрут")
    description = models.TextField("Описание", blank=True, null=True)
    image = models.ImageField("Превью маршрута", upload_to="routes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.image.url)
        return "Нет изображения"

    preview_image.short_description = "Превью"

    def __str__(self):
        return self.name


class Translation(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    language = models.CharField("Язык", max_length=10, choices=[
        ("en", "English"),
        ("ru", "Русский"),
        ("fr", "Français"),
    ])
    text = models.TextField("Перевод", blank=True, null=True)

    def __str__(self):
        return f"{self.language} - {self.text[:30]}"  # Показывать первые 30 символов


