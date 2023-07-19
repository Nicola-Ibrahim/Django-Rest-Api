from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.accounts"
    verbose_name = "Accounts"

    def ready(self) -> None:
        try:
            from .models import signals

        except ImportError:
            pass
