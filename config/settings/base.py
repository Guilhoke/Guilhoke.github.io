from pathlib import Path
import os

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent.parent


SECRET_KEY = "django-insecure-change-this-in-production"

DEBUG = False

ALLOWED_HOSTS = []


# ==============================================================================
# ROTA DE ACESSO AO CMS (Django Admin)
# Por padrão o Django usa "/admin/", um caminho muito previsível e alvo
# constante de varreduras automatizadas. Trocamos por um caminho customizado,
# configurável via variável de ambiente ADMIN_URL — assim o caminho real de
# produção pode ser definido/gerado depois, sem mexer em código.
#
# Isso NÃO substitui autenticação forte (login/senha continuam sendo a
# proteção real) — é só uma camada a mais que tira o painel da mira de bots
# genéricos que testam /admin/ em qualquer domínio.
# ==============================================================================
ADMIN_URL = os.environ.get("ADMIN_URL", "gestao-saude-pirai-x7k2/")


INSTALLED_APPS = [
    # Painel administrativo (tema) — precisa vir antes de django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Projeto
    "core",
    "conteudo",
    "users",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "core" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


MEDIA_URL = "/uploads/"

# Uploads do CMS (ex.: imagens de notícias/eventos) ficam fisicamente dentro
# de core/static, na mesma árvore das imagens que já existiam ali. O prefixo
# de URL (/uploads/) é diferente de STATIC_URL apenas porque o Django exige
# que os dois sejam distintos — não há pasta nem arquivo duplicado, é a
# mesma árvore de diretórios servida por duas rotas.
MEDIA_ROOT = BASE_DIR / "core" / "static"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# PAINEL ADMINISTRATIVO (django-unfold)
# Paleta derivada da identidade visual do site público (core/static/css/estilo.css):
# --cor-primaria (#4b70b6) e --cor-primaria-escura (#3f61a0).
# ==============================================================================

UNFOLD = {
    "SITE_TITLE": "Saúde Digital Piraí",
    "SITE_HEADER": "Saúde Digital Piraí",
    "SITE_SUBHEADER": "Painel Administrativo",
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("img/logo.png"),
    "SITE_LOGO": lambda request: static("img/logo.png"),
    "SITE_SYMBOL": "health_and_safety",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "BORDER_RADIUS": "10px",
    "COLORS": {
        "primary": {
            "50": "242 245 250",
            "100": "226 232 243",
            "200": "201 212 233",
            "300": "161 180 217",
            "400": "115 144 198",
            "500": "75 112 182",    # --cor-primaria (#4b70b6)
            "600": "64 97 159",     # --cor-primaria-escura (#3f61a0)
            "700": "51 78 127",
            "800": "39 58 95",
            "900": "27 41 67",
            "950": "17 25 41",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Visão geral"),
                "separator": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": _("Conteúdo do site"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {
                        "title": _("Notícias"),
                        "icon": "article",
                        "link": reverse_lazy("admin:conteudo_noticia_changelist"),
                    },
                    {
                        "title": _("Eventos"),
                        "icon": "event",
                        "link": reverse_lazy("admin:conteudo_evento_changelist"),
                    },
                    {
                        "title": _("Serviços"),
                        "icon": "medical_services",
                        "link": reverse_lazy("admin:conteudo_servico_changelist"),
                    },
                    {
                        "title": _("Unidades"),
                        "icon": "local_hospital",
                        "link": reverse_lazy("admin:conteudo_unidade_changelist"),
                    },
                ],
            },
            {
                "title": _("Acesso"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Usuários"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": _("Grupos"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}