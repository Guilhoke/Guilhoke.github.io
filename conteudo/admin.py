from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import Evento, Noticia, Servico, Unidade


def preview_thumb(imagem, altura=40):
    if imagem:
        return format_html(
            '<img src="{}" style="height:{}px;border-radius:6px;object-fit:cover;" />',
            imagem.url,
            altura,
        )
    return "—"


def preview_grande(imagem, texto_vazio="Nenhuma imagem enviada ainda."):
    if imagem:
        return format_html(
            '<img src="{}" style="max-height:220px;border-radius:10px;object-fit:cover;" />',
            imagem.url,
        )
    return texto_vazio


@admin.register(Noticia)
class NoticiaAdmin(ModelAdmin):
    list_display = (
        "titulo",
        "preview_imagem",
        "categoria",
        "data_publicacao",
        "publicada",
        "destaque_carrossel",
    )
    list_filter = ("publicada", "destaque_carrossel", "categoria")
    search_fields = ("titulo", "resumo", "categoria")
    date_hierarchy = "data_publicacao"
    ordering = ("-data_publicacao",)
    prepopulated_fields = {"slug": ("titulo",)}
    readonly_fields = ("preview_imagem_grande", "data_criacao")
    compressed_fields = True
    warn_unsaved_form = True

    fieldsets = (
        ("Conteúdo", {
            "fields": ("titulo", "slug", "categoria", "resumo"),
        }),
        ("Imagem", {
            "fields": ("imagem", "preview_imagem_grande"),
        }),
        ("Publicação", {
            "fields": ("publicada", "destaque_carrossel", "data_publicacao", "data_criacao"),
        }),
        ("Link (opcional)", {
            "fields": ("link_externo",),
        }),
    )

    @admin.display(description="Imagem")
    def preview_imagem(self, obj):
        return preview_thumb(obj.imagem)

    @admin.display(description="Pré-visualização")
    def preview_imagem_grande(self, obj):
        return preview_grande(obj.imagem)


@admin.register(Evento)
class EventoAdmin(ModelAdmin):
    list_display = ("titulo", "data", "horario", "local", "publicado")
    list_filter = ("publicado",)
    search_fields = ("titulo", "descricao", "local")
    date_hierarchy = "data"
    ordering = ("data",)
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(Unidade)
class UnidadeAdmin(ModelAdmin):
    list_display = ("nome", "tipo", "preview_imagem", "endereco", "telefone", "ativa")
    list_filter = ("tipo", "ativa")
    search_fields = ("nome", "endereco", "telefone")
    ordering = ("nome",)
    readonly_fields = ("preview_imagem_grande",)
    compressed_fields = True
    warn_unsaved_form = True

    fieldsets = (
        ("Dados da unidade", {
            "fields": ("nome", "tipo", "endereco", "telefone", "ativa"),
        }),
        ("Localização (usada no link 'Ver no Mapa')", {
            "fields": ("latitude", "longitude"),
        }),
        ("Imagem (opcional)", {
            "fields": ("imagem", "preview_imagem_grande"),
            "description": "Se nenhuma imagem for enviada, o site exibe um ícone padrão de acordo com o tipo da unidade.",
        }),
    )

    @admin.display(description="Imagem")
    def preview_imagem(self, obj):
        return preview_thumb(obj.imagem)

    @admin.display(description="Pré-visualização")
    def preview_imagem_grande(self, obj):
        return preview_grande(obj.imagem, texto_vazio="Nenhuma imagem enviada — será usado o ícone padrão do tipo.")


@admin.register(Servico)
class ServicoAdmin(ModelAdmin):
    list_display = ("titulo", "icone", "ordem", "ativo")
    list_editable = ("ordem", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo", "descricao")
    ordering = ("ordem", "titulo")
    warn_unsaved_form = True
