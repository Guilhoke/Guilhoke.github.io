from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def busca(request):
    termo = request.GET.get("q", "").strip().lower()

    resultados = []

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
            "eventos": [],
            "noticias": [],
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
    return render(request, "pages/transparencia.html")


def unidades(request):
    return render(request, "pages/unidades.html")