from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path,
)


handler403 = "core.apps.common.views.errors.tr_handler403"
handler404 = "core.apps.common.views.errors.tr_handler404"
handler500 = "core.apps.common.views.errors.tr_handler500"


urlpatterns = [
    path("secret-admin-panel/", admin.site.urls),
    path("auth/", include("core.apps.authentication.urls")),
    path("", include("core.apps.resumes.urls")),
    path('tinymce/', include('tinymce.urls')),
    path('help/', include('core.apps.help.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
