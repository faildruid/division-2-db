"""Generic models for Division 2 DB App"""

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """Base Model used for Application Models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

