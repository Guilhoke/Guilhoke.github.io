from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    # MEDIA_ROOT aponta para dentro de core/static (mesma pasta das imagens
    # já existentes) — esta rota só serve esses arquivos sob o prefixo
    # /uploads/ em desenvolvimento, sem duplicar nada em disco.
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )