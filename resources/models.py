from django.contrib.auth.models import User
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ForeignKey, ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.search import index


class CuratorIndexPage(Page):
    subpage_types = []
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ResourceIndexPage(Page):
    subpage_types = [
        'resources.AudioResource',
        'resources.ImageResource',
        'resources.QuotationResource',
        'resources.PoetryResource',
        'resources.PrayerResource',
    ]
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ResourceTag(TaggedItemBase):
    content_object = ParentalKey(
        'ResourcePage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ResourceTagIndexPage(Page):
    subpage_types = []

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        resources = ResourcePage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['resources'] = resources
        return context


class ResourcePage(Page):
    parent_page_types = ['resources.ResourceIndexPage']
    subpage_types = []
    date = models.DateField("Updated Date")
    author = models.CharField(max_length=100)
    source = models.URLField()
    description = RichTextField()
    curator = ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    tags = ClusterTaggableManager(
        through=ResourceTag,
        blank=True
    )

    search_fields = Page.search_fields + [
        index.SearchField('author'),
        index.SearchField('description'),
        index.SearchField('source'),
        index.SearchField('tags')
    ]

    source_panels = Page.content_panels + [MultiFieldPanel([
        FieldPanel('author'),
        FieldPanel('source'),
    ])]

    meta_panel = MultiFieldPanel([
        FieldPanel('description'),
        FieldPanel('date'),
        FieldPanel('tags'),
        FieldPanel('curator')
    ])

    content_panels = source_panels + [FieldPanel('description'), meta_panel]


class PoetryResource(ResourcePage):
    poem = RichTextField()

    search_fields = ResourcePage.search_fields + [
        index.SearchField('poem')
    ]

    content_panels = ResourcePage.source_panels + [FieldPanel('poem'), ResourcePage.meta_panel]


class AudioResource(ResourcePage):
    audio = models.FileField()

    content_panels = ResourcePage.content_panels + [FieldPanel('audio')]


class QuotationResource(ResourcePage):
    quotation = RichTextField()

    search_fields = ResourcePage.search_fields + [
        index.SearchField('quotation')
    ]

    content_panels = ResourcePage.source_panels + [FieldPanel('quotation'), ResourcePage.meta_panel]


class ImageResource(ResourcePage):
    image = models.ImageField()

    content_panels = ResourcePage.source_panels + [FieldPanel('image'), ResourcePage.meta_panel]


class PrayerResource(ResourcePage):
    prayer = RichTextField()

    search_fields = ResourcePage.search_fields + [
        index.SearchField('prayer')
    ]

    content_panels = ResourcePage.source_panels + [FieldPanel('prayer'), ResourcePage.meta_panel]
