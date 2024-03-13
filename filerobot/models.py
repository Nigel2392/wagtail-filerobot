from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.images import get_image_model

# Create your models here.

Image = get_image_model()

class DesignState(models.Model):

    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="design_state",
    )

    designstate = models.JSONField(
        verbose_name=_("Design State"),
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
    )
