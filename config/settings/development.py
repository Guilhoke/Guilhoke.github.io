"""
Configuração de DESENVOLVIMENTO.

O banco padrão do projeto é MySQL (ver config/settings/base.py). Para trabalhar
na máquina local sem subir um MySQL, defina USE_SQLITE=1 no .env — o SQLite
volta a ser usado só aqui, nunca em produção.
"""

from .base import *  # noqa: F403
from .base import env_bool


DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "[::1]",
]


# Atalho local: evita exigir um servidor MySQL rodando só para mexer no site.
if env_bool("USE_SQLITE", False):
    DATABASES = {  # noqa: F405
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }
