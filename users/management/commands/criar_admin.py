"""
Cria (ou atualiza) o superusuário do painel a partir do .env.

Existe para que o deploy não dependa de alguém digitar `createsuperuser`
interativamente no servidor — e para que a senha não precise ser digitada em
um terminal cujo histórico fica gravado.

O comando é idempotente: rodar de novo não duplica usuário, apenas garante que
o usuário existe, é superusuário ativo e está com a senha do .env.

Uso:
    python manage.py criar_admin

Variáveis lidas do .env:
    DJANGO_ADMIN_USERNAME   (obrigatória)
    DJANGO_ADMIN_PASSWORD   (obrigatória)
    DJANGO_ADMIN_EMAIL      (opcional)
"""

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Cria ou atualiza o superusuário do painel usando as variáveis do .env."

    def add_arguments(self, parser):
        parser.add_argument(
            "--sem-validacao",
            action="store_true",
            help=(
                "Pula a checagem de força da senha. Use apenas se a política de "
                "senha do Django estiver rejeitando uma senha que você sabe ser forte."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        usuario = os.environ.get("DJANGO_ADMIN_USERNAME")
        senha = os.environ.get("DJANGO_ADMIN_PASSWORD")
        email = os.environ.get("DJANGO_ADMIN_EMAIL", "")

        if not usuario or not senha:
            raise CommandError(
                "Defina DJANGO_ADMIN_USERNAME e DJANGO_ADMIN_PASSWORD no .env "
                "antes de rodar este comando."
            )

        if not options["sem_validacao"]:
            try:
                validate_password(senha)
            except ValidationError as erro:
                raise CommandError(
                    "A senha em DJANGO_ADMIN_PASSWORD foi recusada pelas regras "
                    "de senha do projeto:\n  - " + "\n  - ".join(erro.messages)
                )

        User = get_user_model()

        conta, criada = User.objects.get_or_create(
            username=usuario,
            defaults={"email": email},
        )

        conta.email = email or conta.email
        conta.is_staff = True
        conta.is_superuser = True
        conta.is_active = True
        conta.set_password(senha)
        conta.save()

        if criada:
            self.stdout.write(
                self.style.SUCCESS(f"Superusuário '{usuario}' criado.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superusuário '{usuario}' já existia — senha e permissões atualizadas."
                )
            )

        self.stdout.write(
            self.style.WARNING(
                "Lembre-se: o .env com essa senha não pode ser commitado nem "
                "ficar legível por outros usuários do servidor (chmod 600)."
            )
        )
