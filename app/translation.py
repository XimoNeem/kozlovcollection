from modeltranslation.translator import register, TranslationOptions
from modeltranslation.admin import TranslationAdmin
from .models import VideoSet, Artist, Exhibition, Employee, PostalLink, FlowEvent, Route, Artwork, YearPeriod, PressMention

@register(Artist)
class ArtistTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'photoAuthor', 'textAuthor')

@register(Artwork)
class ArtworkTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'series', 'technique', 'size', 'cipher', 'provenance', 'exhibitions', 'publications')


@register(Exhibition)
class ExhibitionTranslationOptions(TranslationOptions):
    fields = ('title', 'location', 'curators', 'text')

@register(Employee)
class EmployeeTranslationOptions(TranslationOptions):
    fields = ('name', 'position')

@register(PostalLink)
class PostalLinkTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(FlowEvent)
class FlowEventTranslationOptions(TranslationOptions):
    fields = ('text',)

@register(Route)
class RouteTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'full_description', 'article')

@register(YearPeriod)
class YearPeriodTranslationOptions(TranslationOptions):
    fields = ('title', 'text')

@register(PressMention)
class PressMentionTranslationOptions(TranslationOptions):
    fields = ('title', 'author', 'source', 'date')

@register(VideoSet)
class VideoSetTranslationOptions(TranslationOptions):
    fields = ('title',)