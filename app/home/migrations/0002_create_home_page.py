from django.db import migrations


def createHomePage(apps, schema_editor):
    from wagtail.models import Page, Site

    from app.home.models import HomePage

    home_page = HomePage.objects.first()
    if home_page is None:
        root_page = Page.get_first_root_node()
        home_page = HomePage(title="Home", slug="homepage")
        root_page.add_child(instance=home_page)
        home_page.save_revision().publish()

    site = Site.objects.first()
    if site is None:
        Site.objects.create(hostname="localhost", port=8000, root_page=home_page)
        return

    if site.root_page_id != home_page.id:
        site.root_page = home_page
        site.save()


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
        ("wagtailcore", "0096_referenceindex_referenceindex_source_object_and_more"),
    ]

    operations = [
        migrations.RunPython(createHomePage, migrations.RunPython.noop),
    ]
