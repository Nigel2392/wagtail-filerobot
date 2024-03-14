from .utils import notNoneDict
from django.utils.deconstruct import deconstructible

@deconstructible
class Theme:
    def __init__(
            self,
            bg_primary: str = None,
            bg_primary_active: str = None,
            bg_secondary: str = None,
            accent_primary: str = None,
            accent_primary_active: str = None,
            icons_primary: str = None,
            icons_secondary: str = None,
            borders_primary: str = None,
            borders_secondary: str = None,
            borders_strong: str = None,
            light_shadow: str = None,
            warning: str = None,
            font_family: str = None,
        ) -> None:
        
        self.bg_primary = bg_primary
        self.bg_primary_active = bg_primary_active
        self.bg_secondary = bg_secondary
        self.accent_primary = accent_primary
        self.accent_primary_active = accent_primary_active
        self.icons_primary = icons_primary
        self.icons_secondary = icons_secondary
        self.borders_primary = borders_primary
        self.borders_secondary = borders_secondary
        self.borders_strong = borders_strong
        self.light_shadow = light_shadow
        self.warning = warning
        self.font_family = font_family

    def _json(self):
        palette = notNoneDict()
        typography = notNoneDict()
        typography["font-family"]        = self.font_family
        palette["bg-primary"]            = self.bg_primary
        palette["bg-primary-active"]     = self.bg_primary_active
        palette["bg-secondary"]          = self.bg_secondary
        palette["accent-primary"]        = self.accent_primary
        palette["accent-primary-active"] = self.accent_primary_active
        palette["icons-primary"]         = self.icons_primary
        palette["icons-secondary"]       = self.icons_secondary
        palette["borders-primary"]       = self.borders_primary
        palette["borders-secondary"]     = self.borders_secondary
        palette["borders-strong"]        = self.borders_strong
        palette["light-shadow"]          = self.light_shadow
        palette["warning"]               = self.warning

        return {
            "palette": palette,
            "typography": typography,
        }
