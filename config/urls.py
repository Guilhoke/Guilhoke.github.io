from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve


urlpatterns = [
    # O caminho do painel vem de ADMIN_URL (.env), nunca de "admin/".
    # Ver config/settings/base.py.
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

elif getattr(settings, "SERVIR_MEDIA_PELO_DJANGO", False):
    # Em produção, o ideal é o nginx/Apache servir /uploads/ direto do disco
    # (ver README) — é mais rápido e não ocupa um worker do Django por imagem.
    #
    # Enquanto essa regra não existir no servidor web, esta rota evita que as
    # imagens cadastradas pelo painel apareçam quebradas no site. Desligue com
    # SERVIR_MEDIA_PELO_DJANGO=0 assim que o nginx estiver configurado.
    urlpatterns += [
        path(
            settings.MEDIA_URL.lstrip("/") + "<path:path>",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    ]
