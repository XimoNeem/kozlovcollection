import re
import bleach
from django.db import models
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Artist(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    name = models.CharField("Имя", max_length=255)
    photo = models.ImageField("Фото", upload_to="artists/", blank=True, null=True)
    birth_year = models.IntegerField("Год рождения", blank=True, null=True)
    death_year = models.IntegerField("Год смерти", blank=True, null=True)
    description = models.TextField("Описание")
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
    
    def save(self, *args, **kwargs):
        if self.description:
            # Убираем теги <div> в начале и в конце текста
            self.description = self.description.strip()  # Убираем пробелы по краям
            self.description = self.description.lstrip('<div>').rstrip('</div>')  # Убираем <div> в начале и в конце
            
            # Используем bleach для безопасного сохранения разрешенных тегов
            self.description = bleach.clean(self.description, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)

            # Убираем лишние теги в конце текста (например, <br> или <p>)
            self.description = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.description)  # Убираем теги в конце

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ходожника"
        verbose_name_plural = "🧑‍🎨️ Ходожники"

    def __str__(self):
        return self.name

class Artwork(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    main_image = models.ImageField("Главная картинка", upload_to='artworks/main_images/', blank=True, null=True)
    title = models.CharField("Название", max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="artworks")
    series = models.CharField("Серия", max_length=255)
    description = models.TextField("Описание")
    year = models.IntegerField("Год создания", blank=True, null=True)
    technique = models.CharField("Техника", blank=True, null=True)
    size = models.CharField("Размер", blank=True, null=True)
    cipher = models.CharField("Шифр", blank=True, null=True)
    provenance = models.CharField("Провенанс", blank=True, null=True)
    exhibitions = models.CharField("Список выставок", blank=True, null=True)
    publications = models.CharField("Публикации", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_images(self):
        images = self.artwork_images.all()  # Получаем все изображения
        if images.exists():
            return format_html(
                ''.join(f'<img src="{img.image.url}" style="max-height: 100px; margin:5px;"/>' for img in images[:3])
            )
        return "Нет изображений"

    preview_images.short_description = "Превью изображений"

    class Meta:
        verbose_name = "произведение"
        verbose_name_plural = "🎨 Произведения"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.description.strip()
            self.description = self.description.lstrip('<div>').rstrip('</div>')
            self.description = bleach.clean(self.description, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.description = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.description)  
        super().save(*args, **kwargs)

class Exhibition(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    is_own = models.BooleanField("Собственная выставка", default=False)
    image = models.ImageField("Превью выставки", upload_to="routes/", blank=True, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField("Описание")
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    curators = models.CharField()
    catalog_pdf = models.FileField(upload_to='exhibitions/catalogs/', blank=True, null=True)
    press_kit_zip = models.FileField(upload_to='exhibitions/press_kits/', blank=True, null=True)
    artworks = models.ManyToManyField("Artwork", verbose_name="Список работ", blank=True)

    class Meta:
        verbose_name = "выставка"
        verbose_name_plural = "🏺 Выставки"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.text:
            self.text = self.text.strip()
            self.text = self.text.lstrip('<div>').rstrip('</div>')
            self.text = bleach.clean(self.text, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.text = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.text)  
        super().save(*args, **kwargs)

class YearPeriod(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    title = models.CharField(max_length=255)
    text = models.TextField("Места действия")
    artworks = models.ManyToManyField("Artwork", verbose_name="Список работ", blank=True)

    class Meta:
        verbose_name = "год"
        verbose_name_plural = "📅 Годы"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.text:
            self.text = self.text.strip()
            self.text = self.text.lstrip('<div>').rstrip('</div>')
            self.text = bleach.clean(self.text, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.text = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.text)  
        super().save(*args, **kwargs)

class PressMention(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    title = models.CharField("Заголовок", max_length=255)
    link = models.URLField("Ссылка")
    image = models.ImageField("Изображение", upload_to="press_mentions/", blank=True, null=True)
    author = models.CharField("Автор", max_length=255)
    source = models.CharField("Издание", max_length=255)
    date = models.CharField("Дата", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.image.url)
        return "Нет изображения"

    preview_image.short_description = "Превью"
    
    class Meta:
        verbose_name = "упоминание в прессе"
        verbose_name_plural = "📰 Пресса"

    def __str__(self):
        return self.title


class Route(models.Model):
    title = models.CharField("Название маршрута", max_length=255, default="Маршрут")
    short_description = models.CharField("Краткое описание", max_length=500, blank=True, null=True)
    image = models.ImageField("Превью маршрута", upload_to="routes/", blank=True, null=True)
    color = models.CharField("Цвет", max_length=7, default="#FFFFFF")  # HEX-код цвета
    artworks = models.ManyToManyField("Artwork", verbose_name="Список работ", blank=True)
    # videos = models.ManyToManyField(RouteVideo, blank=True, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_description = models.TextField("Полное описание", blank=True, null=True)
    article = models.TextField("Текст статьи", blank=True, null=True)

    def preview_image(self):
        if self.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.image.url)
        return "Нет изображения"

    preview_image.short_description = "Превью"

    class Meta:
        verbose_name = "маршрут"
        verbose_name_plural = "📍 Маршруты"

    def __str__(self):
        return self.title

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="artwork_images")
    image = models.ImageField(upload_to='artworks/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "элемент изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение для {self.artwork.title}"
    
# Сущность PDF-файла для автора
class ArtistPDF(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artist_pdfs")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='artistPDFs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "PDF"
        verbose_name_plural = "📃 PDF авторов"

    def __str__(self):
        return self.title

# Сущность YouTube-видео для автора
class ArtistVideo(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artist_videos")
    title = models.CharField(max_length=255)
    url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "🎥 Видео авторов"
    
    def __str__(self):
        return self.title
    
# Сущность видео для маршрута
class RouteVideo(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_videos")
    title = models.CharField(max_length=255)
    url = models.URLField()
    image = models.ImageField("Превью видео", upload_to="routesVideos/", blank=True, null=True)

    class Meta:
        verbose_name = "видео маршрута"
        verbose_name_plural = "Видео для маршрута"

    def __str__(self):
        return self.title
    
class ExhibitionPDFImage(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="exhibition_pdf_images")
    image = models.ImageField(upload_to='exhibitionPDFImages/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "превью PDF для выставки"
        verbose_name_plural = "PDF"

    def __str__(self):
        return f"Изображение для {self.artwork.title}"
    
class ExhibitionImage(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="artwork_images")
    image = models.ImageField(upload_to='artworks/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "элемент изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение для {self.exhibition.title}"

# Модель сотрудника
class Employee(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='employees/', blank=True, null=True)

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "🧑‍💻️ Сотрудники"

    def __str__(self):
        return self.name

# Модель почтовой ссылки
class PostalLink(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='postal_links/', blank=True, null=True)
    description = models.TextField()
    email = models.EmailField()

    class Meta:
        verbose_name = "почтовый адрес"
        verbose_name_plural = "📪 Почтовые адреса"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.description.strip()
            self.description = self.description.lstrip('<div>').rstrip('</div>')
            self.description = bleach.clean(self.description, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.description = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.description)  
        super().save(*args, **kwargs)

# Модель Flow события
class FlowEvent(models.Model):
    photo = models.ImageField(upload_to='flow_events/', blank=True, null=True)
    text = models.TextField("Текст")

    class Meta:
        verbose_name = "элемент Flow"
        verbose_name_plural = "📸 Flow (Суета)"

    def __str__(self):
        return self.text[:50]
    
    def save(self, *args, **kwargs):
        if self.text:
            self.text = self.text.strip()
            self.text = self.text.lstrip('<div>').rstrip('</div>')
            self.text = bleach.clean(self.text, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.text = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.text)  
        super().save(*args, **kwargs)

