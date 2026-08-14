from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ==============================================================================
# VARIÁVEIS DE AMBIENTE
# Nada sensível (SECRET_KEY, senha do banco, caminho do admin) fica escrito em
# código. Tudo vem do arquivo .env — que está no .gitignore e nunca é commitado.
# Use .env.example como modelo para montar o .env de cada servidor.
# ==============================================================================

load_dotenv(BASE_DIR / ".env")


def env(nome, padrao=None, obrigatoria=False):
    """Lê uma variável de ambiente.

    Com `obrigatoria=True`, a ausência da variável derruba o processo na
    inicialização em vez de deixar o site subir com um valor inseguro —
    é isso que impede um deploy de produção com senha/chave de exemplo.
    """
    valor = os.environ.get(nome, padrao)

    if obrigatoria and not valor:
        raise ImproperlyConfigured(
            f"A variável de ambiente {nome} é obrigatória e não foi definida. "
            f"Copie o .env.example para .env e preencha os valores."
        )

    return valor


def env_bool(nome, padrao=False):
    valor = os.environ.get(nome)

    if valor is None:
        return padrao

    return valor.strip().lower() in ("1", "true", "yes", "on", "sim")


def env_lista(nome, padrao=""):
    """Lê uma variável no formato "a,b,c" e devolve uma lista limpa."""
    bruto = os.environ.get(nome, padrao)

    return [item.strip() for item in bruto.split(",") if item.strip()]


# ==============================================================================
# SEGURANÇA BÁSICA
# ==============================================================================

# Em produção o settings de produção torna esta variável obrigatória.
SECRET_KEY = env("DJANGO_SECRET_KEY", "django-insecure-somente-para-desenvolvimento")

DEBUG = False

ALLOWED_HOSTS = env_lista("DJANGO_ALLOWED_HOSTS")


# ==============================================================================
# ROTA DE ACESSO AO CMS (Django Admin)
#
# Por padrão o Django usa "/admin/", um caminho muito previsível e alvo
# constante de varreduras automatizadas. Aqui o caminho vem sempre da variável
# de ambiente ADMIN_URL, então:
#
#   - o caminho real de produção NÃO está no repositório;
#   - cada ambiente pode ter um caminho diferente;
#   - trocar o caminho é editar o .env e reiniciar, sem tocar em código.
#
# Isso NÃO substitui autenticação forte — login/senha, cookies seguros e
# HTTPS continuam sendo a proteção real (ver config/settings/production.py).
# É uma camada a mais, que tira o painel da mira de bots genéricos.
# ==============================================================================

ADMIN_URL = env("ADMIN_URL", "admin-dev/")

# Normaliza: sem barra no início, com barra no fim — que é o formato que o
# django.urls.path() espera.
ADMIN_URL = ADMIN_URL.strip().lstrip("/")

if not ADMIN_URL.endswith("/"):
    ADMIN_URL += "/"

# Opcional: lista de IPs/faixas com permissão de acessar o painel.
# Vazia = sem restrição por IP (só a rota secreta + login protegem).
ADMIN_IPS_PERMITIDOS = env_lista("ADMIN_IPS_PERMITIDOS")


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

    # Serve os arquivos de /static/ direto pelo Django em produção, com cache
    # e compressão. Precisa vir logo depois do SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # Trava de IP do painel administrativo (só age se ADMIN_IPS_PERMITIDOS
    # estiver preenchida). Depois da autenticação, para poder registrar quem
    # tentou entrar.
    "core.middleware.RestricaoIPAdminMiddleware",
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


# ==============================================================================
# BANCO DE DADOS — MySQL
#
# Todos os parâmetros vêm do .env. O charset utf8mb4 é obrigatório para que
# acentuação e emoji (os ícones dos cards de serviço) sejam gravados corretamente.
#
# sql_mode=STRICT_TRANS_TABLES faz o MySQL recusar dados inválidos em vez de
# truncar silenciosamente — é o comportamento que o Django espera.
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME", "saude_pirai"),
        "USER": env("DB_USER", "root"),
        "PASSWORD": env("DB_PASSWORD", ""),
        "HOST": env("DB_HOST", "127.0.0.1"),
        "PORT": env("DB_PORT", "3306"),
        # Mantém a conexão aberta por 60s entre requisições, em vez de abrir e
        # fechar uma conexão TCP por request.
        "CONN_MAX_AGE": int(env("DB_CONN_MAX_AGE", "60")),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
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


# ==============================================================================
# SESSÃO
# ==============================================================================

# Sessão do painel expira em 8h (um turno de trabalho) e é renovada a cada
# requisição, para não deslogar alguém no meio de um cadastro longo.
SESSION_COOKIE_AGE = int(env("SESSION_COOKIE_AGE", str(8 * 60 * 60)))

SESSION_SAVE_EVERY_REQUEST = True

# Cookies de sessão e CSRF nunca são legíveis por JavaScript.
SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False  # o Django precisa lê-lo para formulários AJAX

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Limite de upload em memória (5 MB). Acima disso o arquivo vai para disco
# temporário, o que evita que um upload gigante consuma a RAM do servidor.
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024


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
