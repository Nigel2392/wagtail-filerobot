from .utils import notNoneDict
from django.utils.deconstruct import deconstructible


@deconstructible
class AnnotationsCommon:
    def __init__(self, 
        fill: str = "#000000",
        stroke: str = "#000000",
        stroke_width: int = 0,
        shadow_offset_x: int = 0,
        shadow_offset_y: int = 0,
        shadow_blur: int = 0,
        shadow_color: str = "#000000",
        shadow_opacity: int = 1,
        opacity: int = 1,
    ):
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.shadow_offset_x = shadow_offset_x
        self.shadow_offset_y = shadow_offset_y
        self.shadow_blur = shadow_blur
        self.shadow_color = shadow_color
        self.shadow_opacity = shadow_opacity
        self.opacity = opacity

    def _json(self):
        d = notNoneDict()
        d["fill"] = self.fill
        d["stroke"] = self.stroke
        d["strokeWidth"] = self.stroke_width
        d["shadowOffsetX"] = self.shadow_offset_x
        d["shadowOffsetY"] = self.shadow_offset_y
        d["shadowBlur"] = self.shadow_blur
        d["shadowColor"] = self.shadow_color
        d["shadowOpacity"] = self.shadow_opacity
        d["opacity"] = self.opacity
        return d
