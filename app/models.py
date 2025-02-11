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

    # Этот метод возвращает список работ художника
    def get_artworks(self):
        return self.artworks.all()

    def preview_image(self):
        if self.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.photo.url)
        return "Нет изображения"
    
    preview_image.short_description = "Превью"

    def __str__(self):
        return self.name


class Artwork(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artworks")  # Ссылка на модель Artist
    year = models.IntegerField("Год создания", blank=True, null=True)
    technique = models.TextField("Техника", blank=True, null=True)  # Описание техники работы
    size = models.TextField("Размер", blank=True, null=True)  # Размер работы
    cipher = models.TextField("Шифр", blank=True, null=True)  # Шифр работы
    provenance = models.TextField("Провенанс", blank=True, null=True)  # История произведения
    exhibitions = models.TextField("Список выставок", blank=True, null=True)  # Список выставок
    publications = models.TextField("Публикации", blank=True, null=True)  # Публикации
    main_image = models.ImageField("Главная картинка", upload_to='artworks/main_images/', blank=True, null=True)  # Главная картинка
    images = models.JSONField("Изображения", blank=True, null=True)  # Список изображений, сохраненных на сервере
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
    short_description = models.CharField("Краткое описание", max_length=500, blank=True, null=True)
    full_description = models.TextField("Полное описание", blank=True, null=True)
    image = models.ImageField("Превью маршрута", upload_to="routes/", blank=True, null=True)
    color = models.CharField("Цвет", max_length=7, default="#FFFFFF")  # HEX-код цвета
    artworks = models.ManyToManyField("Artwork", verbose_name="Список работ", blank=True)
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


