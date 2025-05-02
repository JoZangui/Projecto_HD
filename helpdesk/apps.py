""" app config for helpdesk app """
from django.apps import AppConfig


class HelpdeskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'helpdesk'

    def ready(self):
        """
        This method is called when the app is ready.
        You can import your signals here to ensure they are loaded when the app is ready.
        """
        import helpdesk.signals
