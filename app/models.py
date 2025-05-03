import re
import bleach
from django.db import models
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Artist(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    name = models.CharField("Имя", max_length=255)
    video_name = models.CharField("Название видео", max_length=255, null=True, blank=True)
    video_link = models.URLField("Ссылка на видео", null=True, blank=True)
    video_preview = models.FileField("Превью видео", upload_to='artistVideoImages/', null=True, blank=True)
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
    
    def get_video_shots(self):
        return self.artworks.all()

    def preview_image(self):
        if self.photo:
            return format_html('<img src="{}" style="max-height: 100px;"/>', self.photo.url)
        return "Нет изображения"
    
    def save(self, *args, **kwargs):
        if self.description:
            self.description = self.description.strip()  
            self.description = self.description.lstrip('<div>').rstrip('</div>')
            self.description = bleach.clean(self.description, tags=['br', 'em', 'strong', 'p', 'div'], strip=True)
            self.description = re.sub(r'(<br\s*/?>|<p>|</p>)$', '', self.description)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "ходожника"
        verbose_name_plural = "🧑‍🎨️ Ходожники"

    def __str__(self):
        return self.name
    


class Artwork(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    main_image = models.ImageField("Главная картинка", upload_to='artworks/main_images/', null=True)
    title = models.CharField("Название", max_length=255)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="artworks")
    series = models.CharField("Серия", max_length=255, blank=True, null=True)
    description = models.TextField("Описание")
    year = models.CharField("Год создания", blank=True, null=True, max_length=255)
    technique = models.CharField("Техника", blank=True, null=True, max_length=255)
    size = models.CharField("Размер", blank=True, null=True, max_length=255)
    cipher = models.CharField("Шифр", blank=True, null=True, max_length=255)
    provenance = models.TextField("Провенанс", blank=True, null=True)
    exhibitions = models.TextField("Список выставок", blank=True, null=True)
    publications = models.TextField("Публикации", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # order_desktop = models.PositiveIntegerField("Порядок для десктопа", default=0, db_index=True, blank=True, null=True)
    # order_mobile = models.PositiveIntegerField("Порядок для телефона", default=0, db_index=True, blank=True, null=True)

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
        # ordering = ['order_desktop']
        

    def __str__(self):
        return self.title
    
        
    def get_safe_size(self):
        if not self.size:
            return ""

        value = self.size
        value = re.sub(r'(?<=\d)\s*[xхXX]\s*(?=\d)', ' × ', value)
        parts = value.rsplit(' ', 1)
        if len(parts) == 2:
            value = parts[0] + '\u00A0' + parts[1]

        return value
    
    def get_safe_technique(self):
        if self.technique:
            return self.technique.replace(" ", "\u00A0") 
        else:
            return ""
    
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
    title = models.CharField("Название", max_length=255)
    image = models.ImageField("Превью выставки", upload_to="routes/", blank=True, null=True)
    start_date = models.DateField("Начало выставки")
    end_date = models.DateField("Конец выставки")
    text = models.TextField("Описание")
    location = models.CharField("Место проведения", max_length=255, blank=True, null=True)
    curators = models.CharField("Кураторы", max_length=255, blank=True, null=True)
    # artworks = models.ManyToManyField("Artwork", verbose_name="работы", blank=True)    
    artworks = models.ManyToManyField(
        "Artwork",
        through="PageArtwork",
        verbose_name="работы",
        blank=True
    )

    press_kit_zip = models.FileField(upload_to='exhibitions/press_kits/', blank=True, null=True)
    catalog_pdf = models.FileField(upload_to='exhibitions/catalogs/', blank=True, null=True)

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
    is_null = models.BooleanField("Скрыть контент (включить заглушку)", default=False)
    title = models.CharField("Название", max_length=255)
    text = models.TextField("Места действия")
    # artworks = models.ManyToManyField("Artwork", verbose_name="Работы", blank=True)

    artworks = models.ManyToManyField(
        "Artwork",
        through="YearPeriodArtwork",
        verbose_name="Работы",
        blank=True,
        related_name="year_periods"
    )

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

class Publication(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    title = models.CharField("Название", max_length=255)
    code = models.CharField("Код", max_length=255)
    text = models.CharField("Тексты аннотаций", max_length=255)
    redactor = models.CharField("Тексты аннотаций", max_length=255)
    corrector = models.CharField("Корректор", max_length=255)
    designer = models.CharField("Дизайн, верстка", max_length=255)
    photos = models.CharField("Фотографы", max_length=255)

    class Meta:
        verbose_name = "публикацию"
        verbose_name_plural = "📢 Публикации"

    def __str__(self):
        return self.title

class PressMention(models.Model):
    is_visible = models.BooleanField("Отображается на сайте", default=True)
    title = models.CharField("Заголовок", max_length=255)
    link = models.URLField("Ссылка")
    image = models.ImageField("Изображение", upload_to="press_mentions/", blank=True, null=True)
    author = models.CharField("Автор", max_length=255, blank=True, null=True)
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
    short_description = models.TextField("Краткое описание", blank=True, null=True)
    image = models.ImageField("Превью маршрута", upload_to="routes/", blank=True, null=True)
    color = models.CharField("Цвет", max_length=7, default="#FFFFFF")  # HEX-код цвета
    # artworks = models.ManyToManyField("Artwork", verbose_name="Список работ", blank=True)
    # artworks = models.ManyToManyField("Artwork", verbose_name="Работы", blank=True)
    artworks = models.ManyToManyField(
        "Artwork",
        through="RouteArtwork",
        verbose_name="Работы",
        blank=True,
        related_name="routes"
    )


    route_video = models.ForeignKey("VideoSet", on_delete=models.CASCADE, related_name="route_video", null=True, verbose_name="Видео маршрута")
    # videos = models.ManyToManyField("VideoSet", blank=True, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_description = models.TextField("Полное описание", blank=True, null=True)
    article = models.TextField("Текст статьи", blank=True, null=True)
    article_title = models.CharField("Название статьи", max_length=255, blank=True, null=True)
    article_author = models.CharField("Автор статьи", max_length=255, blank=True, null=True)

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
    video = models.FileField(upload_to='artworks/videos/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "элемент изображения"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение для {self.artwork.title}"
    
class VideoSet(models.Model):
    title = models.CharField("Название блока видео", max_length=255, default="Маршрут")
    color = models.CharField("Цвет", max_length=7, default="#FFFFFF")  # HEX-код цвета

    class Meta:
        verbose_name = "Блок видео для маршрута"
        verbose_name_plural = "🎥 Видео"

    def __str__(self):
        return f"{self.title}"

# Сущность превью (!) YouTube видео для автора
class ArtistVideo(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="artist_video_images")
    image = models.ImageField("Изображение", upload_to='artistPDFsImages/', null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "шот видео"
        verbose_name_plural = "🎥 Шоты из видео"
    
    def __str__(self):
        return f"Превью видео для {self.artist.name}"
    
# Сущность видео для маршрута
class RouteVideo(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_videos")
    image = models.ImageField("Превью видео", upload_to="routesVideos/", blank=True, null=True)

    class Meta:
        verbose_name = "превью видео маршрута"
        verbose_name_plural = "Превью видео для маршрута"

    def __str__(self):
        return self.route.title
    
class RouteImage(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_images")
    image = models.ImageField("Фото маршрута", upload_to="routesImages/", blank=True, null=True)

    class Meta:
        verbose_name = "фото маршрута"
        verbose_name_plural = "Фото для маршрута"

    def __str__(self):
        return self.route.title
    
class ExhibitionPDFImage(models.Model):
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE, related_name="exhibition_pdf_images")
    image = models.ImageField(upload_to='exhibitionPDFImages/images/', verbose_name="изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "превью PDF для выставки"
        verbose_name_plural = "превью PDF"

    def __str__(self):
        return f"Превью PDF для {self.exhibition.title}"
    
class Video(models.Model):
    video_set = models.ForeignKey(VideoSet, on_delete=models.CASCADE, related_name="videos")
    image = models.ImageField(upload_to='videoPreviews/images/', verbose_name="изображение")
    link = models.URLField("Ссылка на видео")

    class Meta:
        verbose_name = "Ссылки на видео вмаршруте"
        verbose_name_plural = "Видео"

    def __str__(self):
        return f"Превью PDF для {self.video_set.title}"
    
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
    order = models.PositiveIntegerField(default=0, blank=False, null=False, db_index=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to='employees/', blank=True, null=True)

    class Meta:
        ordering = ['order']
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

class PageArtwork(models.Model):
    page = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)

    order_desktop = models.PositiveIntegerField("Порядок (десктоп)", default=0, db_index=True)
    order_mobile = models.PositiveIntegerField("Порядок (моб.)", default=0, db_index=True)

    class Meta:
        unique_together = ('page', 'artwork')
        ordering = ['order_desktop']

class YearPeriodArtwork(models.Model):
    period = models.ForeignKey("YearPeriod", on_delete=models.CASCADE, related_name="period_artworks")
    artwork = models.ForeignKey("Artwork", on_delete=models.CASCADE, related_name="year_period_links")

    order_desktop = models.PositiveIntegerField("Порядок (десктоп)", default=0, db_index=True)
    order_mobile = models.PositiveIntegerField("Порядок (моб.)", default=0, db_index=True)

    class Meta:
        unique_together = ('period', 'artwork')
        ordering = ['order_desktop']

class RouteArtwork(models.Model):
    route = models.ForeignKey("Route", on_delete=models.CASCADE, related_name="route_artworks")
    artwork = models.ForeignKey("Artwork", on_delete=models.CASCADE, related_name="route_links")

    order_desktop = models.PositiveIntegerField("Порядок (десктоп)", default=0, db_index=True)
    order_mobile = models.PositiveIntegerField("Порядок (моб.)", default=0, db_index=True)

    class Meta:
        unique_together = ('route', 'artwork')
        ordering = ['order_desktop']

class ArtistArtwork(models.Model):
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE, related_name='artist_links')
    order_desktop = models.PositiveIntegerField("Порядок для десктопа", default=0, db_index=True)
    order_mobile = models.PositiveIntegerField("Порядок для телефона", default=0, db_index=True)

    class Meta:
        unique_together = ('artist', 'artwork')
        ordering = ['order_desktop']