from django.apps import AppConfig


class SupersetIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_superset_integration"
    label = "superset_integration"
