from django.db import models
from django.utils.text import slugify


class Noticia(models.Model):
    titulo = models.CharField("Título", max_length=200)

    resumo = models.TextField(
        "Resumo",
        help_text="Texto curto exibido nos cards de notícia.",
    )

    categoria = models.CharField(
        "Categoria",
        max_length=60,
        blank=True,
        help_text="Selo exibido sobre a notícia (ex.: 'Saúde Digital Piraí').",
    )

    imagem = models.ImageField(
        "Imagem",
        upload_to="img/noticias/",
        help_text="Imagem principal da notícia, usada também no carrossel da Home.",
    )

    data_publicacao = models.DateTimeField("Data de publicação")

    data_criacao = models.DateTimeField("Criada em", auto_now_add=True)

    publicada = models.BooleanField(
        "Publicada",
        default=False,
        help_text="Controla se a notícia aparece no site.",
    )

    destaque_carrossel = models.BooleanField(
        "Destaque no carrossel",
        default=False,
        help_text="Exibe esta notícia no carrossel principal da Home.",
    )

    link_externo = models.URLField(
        "Link externo",
        blank=True,
        help_text="Opcional. Use quando a notícia aponta para um link fora do site.",
    )

    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-data_publicacao"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            contador = 1

            while Noticia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                contador += 1
                slug = f"{base_slug}-{contador}"

            self.slug = slug

        super().save(*args, **kwargs)


class Evento(models.Model):
    titulo = models.CharField("Título", max_length=200)

    descricao = models.TextField("Descrição")

    data = models.DateField("Data do evento")

    horario = models.TimeField("Horário", blank=True, null=True)

    local = models.CharField("Local", max_length=200)

    imagem = models.ImageField(
        "Imagem",
        upload_to="img/eventos/",
        blank=True,
        null=True,
    )

    publicado = models.BooleanField(
        "Publicado",
        default=False,
        help_text="Controla se o evento aparece no site.",
    )

    data_criacao = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["data"]

    def __str__(self):
        return self.titulo


class Unidade(models.Model):
    class TipoUnidade(models.TextChoices):
        HOSPITAL = "Hospital", "Hospital"
        USF = "Unidade de Saúde da Família", "Unidade de Saúde da Família"
        UNIDADE_SAUDE = "Unidade de Saúde", "Unidade de Saúde"
        CENTRO_ESPECIALIZADO = "Centro Especializado", "Centro Especializado"
        PRONTO_SOCORRO = "Pronto Socorro", "Pronto Socorro"
        SERVICO_ESPECIALIZADO = "Serviço Especializado", "Serviço Especializado"
        VIGILANCIA = "Vigilância em Saúde", "Vigilância em Saúde"

    nome = models.CharField("Nome", max_length=150)

    tipo = models.CharField(
        "Tipo",
        max_length=40,
        choices=TipoUnidade.choices,
    )

    endereco = models.CharField("Endereço", max_length=255)

    telefone = models.CharField("Telefone", max_length=20, blank=True)

    latitude = models.DecimalField("Latitude", max_digits=9, decimal_places=6)

    longitude = models.DecimalField("Longitude", max_digits=9, decimal_places=6)

    ativa = models.BooleanField(
        "Ativa",
        default=True,
        help_text="Controla se a unidade aparece na listagem pública.",
    )

    imagem = models.ImageField(
        "Imagem",
        upload_to="img/unidades/",
        blank=True,
        null=True,
        help_text="Opcional. Se não for enviada, o site mostra um ícone padrão conforme o tipo da unidade.",
    )

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Servico(models.Model):
    titulo = models.CharField("Título", max_length=120)

    descricao = models.TextField(
        "Descrição",
        help_text="Texto curto exibido no card, na Home.",
    )

    icone = models.CharField(
        "Ícone",
        max_length=10,
        default="🏥",
        help_text="Um emoji para representar o serviço (ex.: 🏥, 🩺, 🚑, 🧠, 🧪).",
    )

    link = models.CharField(
        "Link",
        max_length=300,
        help_text=(
            "Para onde o card leva ao ser clicado. Pode ser um endereço interno "
            "do site (ex.: /unidades/) ou um link externo completo "
            "(ex.: https://www.netlaudo.com.br/...)."
        ),
    )

    ordem = models.PositiveIntegerField(
        "Ordem de exibição",
        default=0,
        help_text="Cards com número menor aparecem primeiro.",
    )

    ativo = models.BooleanField(
        "Ativo",
        default=True,
        help_text="Controla se o card aparece na Home.",
    )

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["ordem", "titulo"]

    def __str__(self):
        return self.titulo
