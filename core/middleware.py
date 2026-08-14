"""
Middlewares do projeto.
"""

import ipaddress
import logging

from django.conf import settings
from django.http import Http404


logger = logging.getLogger("core.seguranca")


class RestricaoIPAdminMiddleware:
    """Restringe o painel administrativo a uma lista de IPs/faixas.

    Camada opcional, ligada apenas quando ADMIN_IPS_PERMITIDOS está preenchida
    no .env (ex.: "200.150.10.42, 10.0.0.0/8"). Com a lista vazia o middleware
    não faz nada, e a proteção continua sendo a rota secreta + o login.

    A resposta para um IP não autorizado é 404, e não 403: um 403 confirmaria
    ao atacante que existe um painel naquele caminho. O 404 faz a rota parecer
    inexistente, preservando o efeito da URL secreta.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        self.redes = []

        for entrada in getattr(settings, "ADMIN_IPS_PERMITIDOS", []):
            try:
                # strict=False aceita tanto "10.0.0.5" quanto "10.0.0.0/8".
                self.redes.append(ipaddress.ip_network(entrada, strict=False))
            except ValueError:
                logger.warning(
                    "ADMIN_IPS_PERMITIDOS: entrada inválida ignorada: %r", entrada
                )

        self.prefixo_admin = "/" + settings.ADMIN_URL

    def __call__(self, request):
        if self.redes and request.path.startswith(self.prefixo_admin):
            ip = self._ip_do_cliente(request)

            if not self._autorizado(ip):
                logger.warning(
                    "Acesso ao painel bloqueado por IP: %s (caminho %s)",
                    ip,
                    request.path,
                )
                raise Http404

        return self.get_response(request)

    def _autorizado(self, ip):
        if not ip:
            return False

        try:
            endereco = ipaddress.ip_address(ip)
        except ValueError:
            return False

        return any(endereco in rede for rede in self.redes)

    @staticmethod
    def _ip_do_cliente(request):
        """Descobre o IP real do visitante.

        Atrás de proxy, REMOTE_ADDR é o IP do próprio proxy; o IP do visitante
        é o PRIMEIRO item de X-Forwarded-For. Só confiamos nesse cabeçalho
        quando o projeto está declaradamente atrás de um proxy — senão
        qualquer cliente poderia forjá-lo e furar a trava.
        """
        atras_de_proxy = hasattr(settings, "SECURE_PROXY_SSL_HEADER")

        if atras_de_proxy:
            encaminhado = request.META.get("HTTP_X_FORWARDED_FOR", "")

            if encaminhado:
                return encaminhado.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR", "")
