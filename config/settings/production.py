"""
Configuração de PRODUÇÃO.

Este módulo endurece o que o base.py deixa aberto para desenvolvimento.
A regra aqui é: nada sensível tem valor padrão. Se a variável de ambiente
não existir, o processo não sobe — é melhor o deploy falhar na hora do que
o site ficar no ar com chave de exemplo ou com o painel em /admin/.

Ative com:
    DJANGO_SETTINGS_MODULE=config.settings.production
"""

from .base import *  # noqa: F403
from .base import env, env_bool, env_lista


DEBUG = False


# ==============================================================================
# OBRIGATÓRIAS EM PRODUÇÃO
# ==============================================================================

SECRET_KEY = env("DJANGO_SECRET_KEY", obrigatoria=True)

# Caminho do painel: precisa vir do .env. Sem valor padrão, justamente para
# impedir que produção suba com a rota de desenvolvimento.
ADMIN_URL = env("ADMIN_URL", obrigatoria=True).strip().lstrip("/")

if not ADMIN_URL.endswith("/"):
    ADMIN_URL += "/"

# Domínios que o site aceita responder. Sem isso, o Django recusa tudo.
ALLOWED_HOSTS = env_lista("DJANGO_ALLOWED_HOSTS")

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(  # noqa: F405
        "DJANGO_ALLOWED_HOSTS é obrigatória em produção. "
        "Ex.: DJANGO_ALLOWED_HOSTS=saude.pirai.rj.gov.br,www.saude.pirai.rj.gov.br"
    )

# Origens confiáveis para POST (formulários e login do painel). Precisa incluir
# o esquema: https://saude.pirai.rj.gov.br
CSRF_TRUSTED_ORIGINS = env_lista("DJANGO_CSRF_TRUSTED_ORIGINS") or [
    f"https://{host}" for host in ALLOWED_HOSTS if not host.startswith(".")
]


# ==============================================================================
# BANCO DE DADOS
# Em produção a senha do MySQL não pode ficar em branco.
# ==============================================================================

DATABASES["default"]["PASSWORD"] = env("DB_PASSWORD", obrigatoria=True)  # noqa: F405
DATABASES["default"]["NAME"] = env("DB_NAME", obrigatoria=True)  # noqa: F405
DATABASES["default"]["USER"] = env("DB_USER", obrigatoria=True)  # noqa: F405


# ==============================================================================
# HTTPS
#
# SECURE_PROXY_SSL_HEADER só deve ser ligado quando o site está atrás de um
# proxy (nginx, Traefik, Cloudflare) que de fato define X-Forwarded-Proto.
# Ligá-lo sem esse proxy permitiria a um cliente forjar o cabeçalho e fazer o
# Django achar que uma conexão HTTP é HTTPS — por isso fica sob env var.
# ==============================================================================

if env_bool("DJANGO_ATRAS_DE_PROXY", True):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    USE_X_FORWARDED_HOST = True

# Redireciona todo HTTP para HTTPS. Desligue apenas se o proxy já fizer isso.
SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", True)

# HSTS: o navegador passa a recusar HTTP para este domínio.
# Comece com um valor baixo (ex.: 3600) e só suba para 1 ano depois de
# confirmar que o certificado está estável — HSTS não é reversível no prazo.
SECURE_HSTS_SECONDS = int(env("DJANGO_HSTS_SECONDS", str(60 * 60 * 24 * 365)))

SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("DJANGO_HSTS_SUBDOMINIOS", True)

SECURE_HSTS_PRELOAD = env_bool("DJANGO_HSTS_PRELOAD", True)


# ==============================================================================
# COOKIES
# Só trafegam sob HTTPS. É o que impede o roubo da sessão do painel numa rede
# pública (wi-fi de unidade de saúde, por exemplo).
# ==============================================================================

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# Prefixo __Host- : o navegador só aceita o cookie se ele vier por HTTPS, sem
# atributo Domain e com Path=/. Blinda contra subdomínio comprometido
# sobrescrever o cookie de sessão do domínio principal.
SESSION_COOKIE_NAME = "__Host-sessionid"

CSRF_COOKIE_NAME = "__Host-csrftoken"


# ==============================================================================
# CABEÇALHOS DE SEGURANÇA
# ==============================================================================

# Impede o site de ser embutido em <iframe> de terceiros (clickjacking).
X_FRAME_OPTIONS = "DENY"

# Impede o navegador de "adivinhar" o tipo de um arquivo servido.
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# Não vaza a URL do painel para sites externos via Referer.
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"


# ==============================================================================
# ARQUIVOS ESTÁTICOS
# WhiteNoise serve /static/ com hash no nome do arquivo e compressão, para que
# o cache do navegador possa ser eterno sem risco de servir CSS velho.
# ==============================================================================

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Arquivos enviados pelo painel (/uploads/). O ideal é o nginx servir essa
# pasta direto; enquanto isso não estiver configurado, o Django serve —
# assim as imagens das notícias não aparecem quebradas logo no primeiro
# deploy. Ver config/urls.py e a seção de deploy no README.
SERVIR_MEDIA_PELO_DJANGO = env_bool("SERVIR_MEDIA_PELO_DJANGO", True)


# ==============================================================================
# LOGS
# Erros vão para stderr (capturado pelo systemd/Docker) e, se LOG_DIR estiver
# definido, também para arquivo.
# ==============================================================================

LOG_DIR = env("LOG_DIR")

_handlers = ["console"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": _handlers,
            "level": env("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        # Registra tentativa de acesso ao painel a partir de IP não autorizado.
        "core.seguranca": {
            "handlers": _handlers,
            "level": "INFO",
            "propagate": False,
        },
    },
}

if LOG_DIR:
    LOGGING["handlers"]["arquivo"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": str(Path(LOG_DIR) / "django.log"),  # noqa: F405
        "maxBytes": 5 * 1024 * 1024,
        "backupCount": 5,
        "formatter": "verbose",
    }

    for logger in LOGGING["loggers"].values():
        logger["handlers"] = _handlers + ["arquivo"]


# ==============================================================================
# E-MAIL (relatório de erro 500 para os administradores)
# Opcional: só é configurado se EMAIL_HOST estiver no .env.
# ==============================================================================

if env("EMAIL_HOST"):
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_PORT = int(env("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)

    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    ADMINS = [
        ("Equipe", endereco) for endereco in env_lista("DJANGO_ADMIN_EMAILS")
    ]
