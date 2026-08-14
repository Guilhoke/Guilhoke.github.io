from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from conteudo.models import Evento, Noticia, Servico, Unidade


# Quantos slides o carrossel da Home exibe, no máximo.
MAX_SLIDES_CARROSSEL = 5

# Portal de transparência da prefeitura (o município não hospeda essa página).
URL_TRANSPARENCIA = "https://transparencia.pirai.rj.gov.br/"


def _noticias_do_carrossel():
    """Monta a lista de slides do carrossel da Home.

    A fonte principal são as notícias marcadas como "Destaque no carrossel"
    no painel. Quando há menos de duas marcadas, o carrossel não teria o que
    alternar e a Home ficaria com uma imagem estática — então completamos com
    as notícias publicadas mais recentes, sem repetir as que já entraram.

    Marcar duas ou mais notícias como destaque volta a dar controle total
    sobre o que aparece e em que ordem.
    """
    destaques = list(
        Noticia.objects.filter(
            publicada=True,
            destaque_carrossel=True,
        )[:MAX_SLIDES_CARROSSEL]
    )

    if len(destaques) >= 2:
        return destaques

    ja_incluidas = [noticia.pk for noticia in destaques]

    complemento = Noticia.objects.filter(publicada=True).exclude(
        pk__in=ja_incluidas
    )[: MAX_SLIDES_CARROSSEL - len(destaques)]

    return destaques + list(complemento)


def home(request):
    return render(
        request,
        "pages/home.html",
        {
            "noticias": _noticias_do_carrossel(),
            "servicos": Servico.objects.filter(ativo=True),
            "noticias_recentes": Noticia.objects.filter(publicada=True)[:5],
            "eventos_recentes": Evento.objects.filter(
                publicado=True,
                data__gte=timezone.localdate(),
            )[:5],
        },
    )


def busca(request):
    termo = request.GET.get("q", "").strip()

    resultados = []

    if termo:
        eventos_url = reverse("eventos")
        unidades_url = reverse("unidades")

        noticias_encontradas = Noticia.objects.filter(
            Q(publicada=True)
            & (
                Q(titulo__icontains=termo)
                | Q(resumo__icontains=termo)
                | Q(categoria__icontains=termo)
            )
        )

        for noticia in noticias_encontradas:
            resultados.append({
                "tipo": "Notícia",
                "titulo": noticia.titulo,
                "descricao": noticia.resumo,
                "link": noticia.link_externo or eventos_url,
            })

        eventos_encontrados = Evento.objects.filter(
            Q(publicado=True)
            & (
                Q(titulo__icontains=termo)
                | Q(descricao__icontains=termo)
                | Q(local__icontains=termo)
            )
        )

        for evento in eventos_encontrados:
            resultados.append({
                "tipo": "Evento",
                "titulo": evento.titulo,
                "descricao": evento.descricao,
                "link": eventos_url,
            })

        unidades_encontradas = Unidade.objects.filter(
            Q(ativa=True)
            & (
                Q(nome__icontains=termo)
                | Q(endereco__icontains=termo)
                | Q(tipo__icontains=termo)
            )
        )

        for unidade in unidades_encontradas:
            resultados.append({
                "tipo": "Unidade de Saúde",
                "titulo": unidade.nome,
                "descricao": f"{unidade.tipo} — {unidade.endereco}",
                "link": unidades_url,
            })

    return render(
        request,
        "pages/busca.html",
        {
            "termo": termo,
            "resultados": resultados,
        }
    )


def duvidas(request):
    return render(request, "pages/duvidas.html")


def eventos(request):
    return render(
        request,
        "pages/eventos.html",
        {
            "eventos": Evento.objects.filter(publicado=True),
            "noticias": Noticia.objects.filter(publicada=True),
        },
    )


def ouvidoria(request):
    return render(request, "pages/ouvidoria.html")


def profissionais(request):
    return render(request, "pages/profissionais.html")


def servicos(request):
    return render(request, "pages/servicos.html")


def servidor(request):
    return render(request, "pages/servidor.html")


def transparencia(request):
    # Não existe uma página de transparência dentro deste site — o conteúdo
    # fica no portal da prefeitura, que é para onde o menu do cabeçalho já
    # aponta. Esta rota existe porque o rodapé e a página de dúvidas usam
    # {% url 'transparencia' %}; ela redireciona em vez de tentar renderizar
    # um template inexistente (que virava erro 500 com DEBUG=False).
    return redirect(URL_TRANSPARENCIA)


def unidades(request):
    return render(
        request,
        "pages/unidades.html",
        {
            "unidades": Unidade.objects.filter(ativa=True),
        },
    )