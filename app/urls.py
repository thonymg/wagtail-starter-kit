from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from app.search import views as search_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("home/", RedirectView.as_view(url="/", permanent=False)),
    path("welcome/", RedirectView.as_view(url="/", permanent=False)),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("api/search/", search_views.search_api, name="search-api"),
    path("style-guide/", include("app.style_guide.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    path("", include(wagtail_urls)),
]
