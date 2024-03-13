from django.forms import widgets
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.templatetags.static import static
import json

from wagtail.images import get_image_model

from .theme import Theme

Image = get_image_model()


class HTMLMediaSource:
    def __init__(self, src: str, type: str) -> None:
        self.src = src
        self.type = type

    def __html__(self) -> str:
        src = self.src
        if not src.startswith("http") and not src.startswith("/"):
            src = static(src)
            
        return format_html(
            '<script src="{}" type="{}"></script>',
            src,
            self.type,
        )

DEFAULT_TABS = [
    "Finetune",
    "Filters",
    "Adjust",
    "Watermark",
    "Annotate",
    "Resize",
]


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return obj.to_json()
        elif hasattr(obj, "_json"):
            return obj._json()
        return super().default(obj)


_vars = [
    "default_tab_index",
    "default_tool_index",
    "use_backend_translations",
    "language",
    "avoid_changes_not_saved_alert_on_leave",
    "default_saved_image_quality",
    "force_to_png_in_elliptical_crop",
    "use_cloud_image",
    "saving_pixel_ratio",
    "preview_pixel_ratio",
    "observe_plugin_container_size",
    "show_canvas_only",
    "use_zoom_presets_menu",
    "disable_zooming",
    "no_cross_origin",
    "disable_save_if_no_changes",
]

_tpl_data = [
    ("tabs", "tabs"),
    ("theme", "theme"),
    ("annotationsCommon", "annotations_common"),
    ("Text", "text"),
    ("Image", "image"),
    ("Rect", "rect"),
    ("Ellipse", "ellipse"),
    ("Polygon", "polygon"),
    ("Pen", "pen"),
    ("Line", "line"),
    ("Arrow", "arrow"),
    ("Watermark", "watermark"),
    ("Rotate", "rotate"),
    ("Crop", "crop"),
    ("CropPresetFolder", "crop_preset_folder"),
    ("CropPresetGroup", "crop_preset_group"),
    ("CropPresetItem", "crop_preset_item"),
    ("cloudimage", "cloud_image"),
]


def _json_script(data, id: str) -> str:
    if not data:
        return ""
    
    return format_html(
        '<script type="application/json" id="{}">{}</script>',
        id,
        mark_safe(json.dumps(data, cls=_JSONEncoder)),
    )

class FileRobotWidget(widgets.NumberInput):
    input_type = "hidden"
    template_name = "filerobot/widgets/file_robot_widget.html"

    def __init__(self,
            tabs: list[str] = None,
            theme: Theme = None,
            annotations_common: dict = None,
            text: dict = None,
            image: dict = None,
            rect: dict = None,
            ellipse: dict = None,
            polygon: dict = None,
            pen: dict = None,
            line: dict = None,
            arrow: dict = None,
            watermark: dict = None,
            rotate: dict = None,
            crop: dict = None,
            crop_preset_folder: dict = None,
            crop_preset_group: dict = None,
            crop_preset_item: dict = None,
            cloud_image: dict = None,

            default_tab_index: int = None,
            default_tool_index: int = None,
            use_backend_translations: bool = None,
            language: str = None,
            avoid_changes_not_saved_alert_on_leave: bool = None,
            default_saved_image_quality: int = None,
            force_to_png_in_elliptical_crop: bool = None,
            use_cloud_image: bool = None,
            saving_pixel_ratio: int = None,
            preview_pixel_ratio: int = None,
            observe_plugin_container_size: bool = None,
            show_canvas_only: bool = None,
            use_zoom_presets_menu: bool = None,
            disable_zooming: bool = None,
            no_cross_origin: bool = None,
            disable_save_if_no_changes: bool = None,
            attrs: dict = None,
        ) -> None:

        self.tabs = tabs or DEFAULT_TABS
        self.theme = theme
        self.annotations_common = annotations_common
        self.text = text
        self.image = image
        self.rect = rect
        self.ellipse = ellipse
        self.polygon = polygon
        self.pen = pen
        self.line = line
        self.arrow = arrow
        self.watermark = watermark
        self.rotate = rotate
        self.crop = crop
        self.crop_preset_folder = crop_preset_folder
        self.crop_preset_group = crop_preset_group
        self.crop_preset_item = crop_preset_item
        self.cloud_image = cloud_image

        self.default_tab_index = default_tab_index
        self.default_tool_index = default_tool_index
        self.use_backend_translations = use_backend_translations
        self.language = language
        self.avoid_changes_not_saved_alert_on_leave = avoid_changes_not_saved_alert_on_leave
        self.default_saved_image_quality = default_saved_image_quality
        self.force_to_png_in_elliptical_crop = force_to_png_in_elliptical_crop
        self.use_cloud_image = use_cloud_image
        self.saving_pixel_ratio = saving_pixel_ratio
        self.preview_pixel_ratio = preview_pixel_ratio
        self.observe_plugin_container_size = observe_plugin_container_size
        self.show_canvas_only = show_canvas_only
        self.use_zoom_presets_menu = use_zoom_presets_menu
        self.disable_zooming = disable_zooming
        self.no_cross_origin = no_cross_origin
        self.disable_save_if_no_changes = disable_save_if_no_changes

        super().__init__(attrs=attrs)

    def get_context(self, name: str, value, attrs):
        context = super().get_context(name, value, attrs)
        attrs = context["widget"]["attrs"]
        id_attr = attrs["id"]
        if id_attr:
            tpl_data = []
            for tpl, attribute_name in _tpl_data:
                tpl_data.append(_json_script(
                    data=getattr(self, attribute_name),
                    id=f"{id_attr}-{tpl}",
                ))
            context["widget"]["tpl_data"] = tpl_data
        return context

    def build_attrs(self, base_attrs, extra_attrs = None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            "data-controller": "file-robot-widget",
            "data-file-robot-widget-submit-value": reverse(
                "filerobot:file_view"
            ),
        })

        for var in _vars:
            value = getattr(self, var)
            var = var.replace("_", "-")
            if value is not None:
                attrs[f"data-file-robot-widget-{var}-value"] = json.dumps(
                    obj=value,
                    cls=_JSONEncoder,
                )

        return attrs
    
    def get_value_data(self, value):
        if value is None:
            return None
        
        return value.pk

    class Media:
        css = {
            "all": (
                "filerobot/css/filerobot_widget.css",
            )
        }
        js = (
            "filerobot/js/filerobot.js",
            "filerobot/js/file_robot_widget_controller.js",
            "filerobot/js/file_robot_widget.js",
        )
