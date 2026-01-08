from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.shortcuts import render

class BlogIndexPage(Page):
    """Index des articles du blog."""

    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    subpage_types = ['blog.BlogPage']
    parent_page_types = ['home.HomePage']

    def serve(self, request):
        page_number = request.GET.get('page', 1)

        posts = BlogPage.objects.child_of(self).live().order_by('-date')
        paginator = Paginator(posts, 2)
        posts = paginator.get_page(page_number)

        context = self.get_context(request)
        context['posts'] = posts

        print(posts.object_list)

        print(f"DEBUG: Headers keys: {list(request.headers.keys())}")
        if request.headers.get("HX-Request"):
            print("DEBUG: HTMX Request detected!")
            return render(request, 'blog/partials/blog_list_items.html', context)

        return render(request, 'blog/blog_index_page.html', context)

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
