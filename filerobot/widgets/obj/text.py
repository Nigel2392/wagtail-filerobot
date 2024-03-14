from .utils import notNoneDict
from django.utils.deconstruct import deconstructible

@deconstructible
class Text:
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
    ):
        self.text           = text
        self.font_family    = font_family
        self.fonts          = fonts
        self.font_size      = font_size
        self.letter_spacing = letter_spacing
        self.line_height    = line_height
        self.align          = align
        self.font_style     = font_style

    def _json(self):
        d = notNoneDict()
        d["text"]          = self.text
        d["fontFamily"]    = self.font_family
        d["fonts"]         = self.fonts
        d["fontSize"]      = self.font_size
        d["letterSpacing"] = self.letter_spacing
        d["lineHeight"]    = self.line_height
        d["align"]         = self.align
        d["fontStyle"]     = self.font_style
        return d
