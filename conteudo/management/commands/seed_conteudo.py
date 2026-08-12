"""
Comando de carga inicial (seed).

Migra os dados atualmente hardcoded em `core/data/noticias.py`,
`core/data/servicos.py` e `core/data/unidades.py` para o banco, usando
os Models definitivos.

Este comando existe apenas para popular o ambiente durante a transição.
Ele não deve ser usado como fonte de verdade contínua — depois da carga
inicial, todo o conteúdo passa a ser gerenciado pelo Django Admin.

Uso:
    python manage.py seed_conteudo
"""

from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from core.data.noticias import NOTICIAS
from core.data.servicos import SERVICOS
from core.data.unidades import UNIDADES
from conteudo.models import Noticia, Servico, Unidade


class Command(BaseCommand):
    help = "Popula o banco com os dados temporários de core/data/*.py"

    def handle(self, *args, **options):
        self.seed_unidades()
        self.seed_servicos()
        self.seed_noticias()

    def seed_unidades(self):
        criadas = 0

        for item in UNIDADES:
            _, foi_criada = Unidade.objects.get_or_create(
                nome=item["nome"],
                defaults={
                    "tipo": item["tipo"],
                    "endereco": item["endereco"],
                    "telefone": item.get("telefone", ""),
                    "latitude": item["lat"],
                    "longitude": item["lng"],
                    "ativa": True,
                },
            )
            if foi_criada:
                criadas += 1

        self.stdout.write(
            self.style.SUCCESS(f"Unidades: {criadas} criada(s), {len(UNIDADES) - criadas} já existente(s).")
        )

    def seed_servicos(self):
        criadas = 0

        for item in SERVICOS:
            _, foi_criada = Servico.objects.get_or_create(
                titulo=item["titulo"],
                defaults={
                    "descricao": item["descricao"],
                    "icone": item["icone"],
                    "link": item["link"],
                    "ordem": item["ordem"],
                    "ativo": True,
                },
            )
            if foi_criada:
                criadas += 1

        self.stdout.write(
            self.style.SUCCESS(f"Serviços: {criadas} criado(s), {len(SERVICOS) - criadas} já existente(s).")
        )

    def seed_noticias(self):
        # As imagens já existem fisicamente em core/static/img/noticias/, e o
        # ImageField aponta para essa mesma pasta (upload_to="img/noticias/").
        # Por isso, aqui só referenciamos o nome do arquivo existente — sem
        # copiar bytes, sem duplicar dado.
        criadas = 0
        puladas_sem_imagem = []

        for item in NOTICIAS:
            if Noticia.objects.filter(titulo=item["titulo"]).exists():
                continue

            nome_arquivo = item["imagem"].split("/")[-1]
            caminho_relativo_ao_static = f"img/noticias/{nome_arquivo}"

            if not (
                Noticia._meta.get_field("imagem").storage.exists(caminho_relativo_ao_static)
            ):
                puladas_sem_imagem.append(item["titulo"])
                continue

            noticia = Noticia(
                titulo=item["titulo"],
                resumo=item["titulo"],
                categoria="Saúde Digital Piraí",
                data_publicacao=make_aware(datetime.now()),
                publicada=True,
                destaque_carrossel=True,
                link_externo="" if item.get("link") in (None, "#") else item["link"],
            )
            noticia.imagem.name = caminho_relativo_ao_static
            noticia.save()
            criadas += 1

        self.stdout.write(
            self.style.SUCCESS(f"Notícias: {criadas} criada(s).")
        )

        if criadas:
            self.stdout.write(
                self.style.WARNING(
                    "Atenção: 'resumo' foi preenchido automaticamente com o "
                    "título (os dados antigos não tinham esse campo). Revise "
                    "e ajuste o texto pelo Admin antes de publicar de verdade."
                )
            )

        if puladas_sem_imagem:
            self.stdout.write(
                self.style.WARNING(
                    "As notícias abaixo não foram criadas por falta da imagem "
                    "em core/static/img/noticias/. Cadastre-as manualmente pelo "
                    "Admin com o upload da imagem correta:"
                )
            )
            for titulo in puladas_sem_imagem:
                self.stdout.write(f"  - {titulo}")
