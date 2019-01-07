from django.conf import settings
from django.urls import re_path, include
from django.views import generic as generic_views
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from django.urls import path, re_path, include

urlpatterns = [
    re_path(r'^$', generic_views.TemplateView.as_view(
        template_name='landing_page.html'),
        name='landing_page'),
    # Wagtail
    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^wagtail/', include(wagtail_urls)),
    re_path(r'^notifications/', include('django_nyt.urls')),
    re_path(r'^wiki/', include('wiki.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
