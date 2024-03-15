from typing import TypeVar
from django.utils.deconstruct import deconstructible as _deconstructible

from ..constants import (
    TABS_IDS as TABS,
    TOOLS_IDS as TOOLS,
)
from ..utils import (
    notNoneDict,
    camelize,
)

_T = TypeVar("_T")

def deconstructible(*args: _T, path=None) -> _T:
    return _deconstructible(*args, path=path)


class _JSONable:
    _key_fmt = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def _json(self):
        return notNoneDict(self.kwargs)


@deconstructible
class AnnotationsCommon(_JSONable):
    _key_fmt = camelize

    def __init__(self, 
        # Defaults as specified by filerobot readme.
        fill:            str = None, # "#000000",
        stroke:          str = None, # "#000000",
        stroke_width:    int = None, # 0,
        shadow_offset_x: int = None, # 0,
        shadow_offset_y: int = None, # 0,
        shadow_blur:     int = None, # 0,
        shadow_color:    str = None, # "#000000",
        shadow_opacity:  int = None, # 1,
        opacity:         int = None, # 1,
    ):
        super().__init__(
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            shadow_offset_x=shadow_offset_x,
            shadow_offset_y=shadow_offset_y,
            shadow_blur=shadow_blur,
            shadow_color=shadow_color,
            shadow_opacity=shadow_opacity,
            opacity=opacity,
        )

def _make_theme(typography: str):
    d = {
        # We handle the color palette in CSS to style it the Wagtail way.
        "palette": {
            "bg-primary":             "unset",
            "bg-primary-active":      "unset",
            "bg-secondary":           "unset",
            "accent-primary":         "hsl(180.5 100% 24.7%)",
            "accent-primary-active":  "unset",
            "icons-primary":          "unset",
            "icons-secondary":        "unset",
            "borders-primary":        "unset",
            "borders-secondary":      "unset",
            "borders-strong":         "unset",
            "light-shadow":           "unset",
            "warning":                "unset",
        }
    }

    if typography:
        d["typography"] = {
            "font-family": typography
        }

    return d



@deconstructible
class Text(AnnotationsCommon):
    def __init__(
        self,
        text:           str       = None,
        font_family:    str       = None,
        fonts:          list[str] = None,
        font_size:      int       = None,
        letter_spacing: int       = None,
        line_height:    int       = None,
        align:          str       = None,
        font_style:     str       = None,
        **annotationsCommon,
    ):
        super().__init__(
            text           = text,
            font_family    = font_family,
            fonts          = fonts,
            font_size      = font_size,
            letter_spacing = letter_spacing,
            line_height    = line_height,
            align          = align,
            font_style     = font_style,
            **annotationsCommon,
        )


@deconstructible
class ImageObject(_JSONable):
    _key_fmt = camelize

    def __init__(self, original_url: str = None, preview_url: str = None):
        super().__init__(
            original_url=original_url,
            preview_url=preview_url,
        )

@deconstructible
class Image(AnnotationsCommon):
    def __init__(
            self,
            fill: str = None,
            disable_upload: bool = False,
            gallery: list[ImageObject] = None,
            **annotationsCommon,
        ) -> None:

        super().__init__(
            fill                = fill,
            disable_upload      = disable_upload,
            gallery             = gallery,
            **annotationsCommon
        )
    
@deconstructible
class Rect(AnnotationsCommon):
    def __init__(
            self,
            corner_radius: int = None,
            **annotationsCommon,
        ) -> None:

        super().__init__(
            corner_radius = corner_radius,
            **annotationsCommon
        )

@deconstructible
class Ellipse(AnnotationsCommon):
    pass

@deconstructible
class Polygon(AnnotationsCommon):
    def __init__(
            self,
            sides: int = None,
            **annotationsCommon,
        ) -> None:

        super().__init__(sides = sides, **annotationsCommon)

@deconstructible
class Pen(AnnotationsCommon):
    def __init__(
            self,
            stroke_width:                     int   = None, # None,
            tension:                          float = None, # 0.5,
            line_cap:                         str   = None, # 'round',
            select_annotation_after_drawing:  bool  = None, # True,
            **annotationsCommon,
        ) -> None:

        super().__init__(
            stroke_width                    = stroke_width,
            tension                         = tension,
            line_cap                        = line_cap,
            select_annotation_after_drawing = select_annotation_after_drawing,
            **annotationsCommon
        )

@deconstructible
class Line(AnnotationsCommon):
    def __init__(
            self,
            stroke_width: int = None,
            line_cap:     str = None,
            **annotationsCommon,
        ) -> None:

        super().__init__(
            stroke_width = stroke_width,
            line_cap     = line_cap,
            **annotationsCommon
        )

@deconstructible
class Arrow(Line):
    def __init__(self,
            stroke_width:   int = None,
            line_cap:       str = None,
            pointer_length: int = None,
            pointer_width:  int = None,
            **annotationsCommon
        ) -> None:

        super().__init__(
            stroke_width   = stroke_width,
            line_cap       = line_cap,
            pointer_length = pointer_length,
            pointer_width  = pointer_width,
            **annotationsCommon
        )

@deconstructible
class WatermarkImageObject(_JSONable):
    _key_fmt = camelize

    def __init__(self,
            url: str = None,
            preview_url:  str = None,
            **kwargs,
        ) -> None:
        
        super().__init__(
            url=url,
            preview_url=preview_url,
            **kwargs
        )

@deconstructible
class Watermark(_JSONable):
    _key_fmt = camelize

    def __init__(self,
                gallery:             list[WatermarkImageObject] = None,
                text_scaling_ratio:  float                      = None,
                image_scaling_ratio: float                      = None,
                hide_text_watermark: bool                       = None,
                # onUploadWatermarkImgClick js func
            ):
        super().__init__(
            gallery             = gallery,
            text_scaling_ratio  = text_scaling_ratio,
            image_scaling_ratio = image_scaling_ratio,
            hide_text_watermark = hide_text_watermark,
        )
