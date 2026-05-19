from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.template.response import TemplateResponse
from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    if search_query:
        search_results = Page.objects.live().search(search_query)
    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )


def search_api(request):
    """JSON endpoint consumed by the SearchBar Vue island."""
    query = request.GET.get("query", "").strip()

    if not query:
        return JsonResponse({"results": [], "total": 0})

    raw_results = Page.objects.live().search(query)

    results = [
        {
            "id": page.id,
            "title": page.title,
            "url": page.get_url(request),
            "description": page.search_description or "",
        }
        for page in raw_results[:10]
    ]

    return JsonResponse({"results": results, "total": len(results)})
