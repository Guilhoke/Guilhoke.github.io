from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("busca/", views.busca, name="busca"),
    path("duvidas/", views.duvidas, name="duvidas"),
    path("eventos/", views.eventos, name="eventos"),
    path("ouvidoria/", views.ouvidoria, name="ouvidoria"),
    path("profissionais/", views.profissionais, name="profissionais"),
    path("servicos/", views.servicos, name="servicos"),
    path("servidor/", views.servidor, name="servidor"),
    path("transparencia/", views.transparencia, name="transparencia"),
    path("unidades/", views.unidades, name="unidades"),
]