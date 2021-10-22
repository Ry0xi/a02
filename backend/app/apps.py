from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

# new =>
    def ready(self):
        """
        This function is called when startup.
        """
        from .task_over import start # <= さっき作った start関数をインポート
        start()
