from typing import TYPE_CHECKING
from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.images import get_image_model

if TYPE_CHECKING:
    from wagtail.images.models import (
        Image as WagtailImage,
    )



Image = get_image_model()


class DesignState(models.Model):

    image: "WagtailImage" = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="design_state",
    )

    designstate: dict = models.JSONField(
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

    class Meta:
        verbose_name = _("Design State")
        verbose_name_plural = _("Design States")
        ordering = ("-updated_at",)
        
