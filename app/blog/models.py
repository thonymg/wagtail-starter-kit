from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.utils.text import slugify

class BlogIndexPage(Page):
    """Index des articles du blog."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['blog.BlogPage']
    parent_page_types = ['home.HomePage']

class BlogPage(Page):
    """Page d'article de blog individuelle."""

    date = models.DateField("Date de publication")
    intro = models.CharField(max_length=250)
    body = RichTextField()

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []
