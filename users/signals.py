from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging
from django.utils import timezone

# O logger é um objeto que permite registrar mensagens de log em diferentes níveis (debug, info, warning, error, critical).
logger = logging.getLogger('helpdesk')

@receiver(user_logged_in)
def log_login_signal(sender, request, user, **kwargs):
    """
    Signal receiver for user login.
    Logs the login event with the current timestamp.
    """
    # O {request.META['REMOTE_ADDR']} é usado para capturar o endereço IP do cliente (ou seja, do dispositivo que fez a solicitação) em uma aplicação Django. No contexto do log.
    # Isso é útil para registrar informações sobre a origem do acesso, como o endereço IP do usuário que está fazendo login.
    # Isso pode ser útil para fins de auditoria, segurança ou análise de tráfego.
    
    # Em alguns casos, o endereço IP pode ser mascarado por proxies ou redes NAT (Network Address Translation). Se isso acontecer, você pode precisar usar o cabeçalho 'HTTP_X_FORWARDED_FOR' para obter o endereço IP original.
    # Isso pode ser feito verificando se o cabeçalho existe e, em caso afirmativo, usando seu valor.
    # Exemplo: request.META.get('HTTP_X_FORWARDED_FOR', request.META['REMOTE_ADDR'])
    # Isso garante que você obtenha o endereço IP correto, mesmo que o usuário esteja por trás de um proxy.
    # -----------------------------------------------------------------
    # O {timezone.now()} é usado para capturar a data e hora atual no fuso horário configurado na aplicação Django.
    # Isso é útil para registrar quando o evento de login ocorreu.

    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]  # Pega o primeiro IP da lista
    else:
        ip = request.META.get('REMOTE_ADDR')

    logger.info(f"User {user.username} logged in at {timezone.now()} in {ip}")

@receiver(user_logged_out)
def log_logout_signal(sender, request, user, **kwargs):
    """
    Signal receiver for user logout.
    Logs the logout event with the current timestamp.
    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        ip = ip.split(',')[0]  # Pega o primeiro IP da lista
    else:
        ip = request.META.get('REMOTE_ADDR')

    logger.info(f"User {user.username} logged out at {timezone.now()} in {ip}")
