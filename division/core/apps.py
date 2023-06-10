"""Configuration for the Core App."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """CoreConfig."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "division.core"
    label = "division_core"
