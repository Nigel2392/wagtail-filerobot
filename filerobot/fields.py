from typing import Any
from django.db import models
from wagtail.images import get_image_model_string
from .forms import FileRobotField as FileRobotFormField
from .widgets import FileRobotWidget, Theme




class FileRobotField(models.ForeignKey):
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

            # Common fields to help the editor with autocompletion
            verbose_name=None,
            unique=False,
            blank=True,
            null=True,
            help_text="",
            validators=(),
            on_delete=models.CASCADE,

            # Deconstruct utility to avoid re-typing every field
            widget_kwargs=None,
            
            *args, **kwargs
        ):
        to = get_image_model_string()

        self.widget_kwargs = widget_kwargs or {
            "tabs": tabs,
            "theme": theme,
            "annotations_common": annotations_common,
            "text": text,
            "image": image,
            "rect": rect,
            "ellipse": ellipse,
            "polygon": polygon,
            "pen": pen,
            "line": line,
            "arrow": arrow,
            "watermark": watermark,
            "rotate": rotate,
            "crop": crop,
            "crop_preset_folder": crop_preset_folder,
            "crop_preset_group": crop_preset_group,
            "crop_preset_item": crop_preset_item,
            "cloud_image": cloud_image,
            "default_tab_index": default_tab_index,
            "default_tool_index": default_tool_index,
            "use_backend_translations": use_backend_translations,
            "language": language,
            "avoid_changes_not_saved_alert_on_leave": avoid_changes_not_saved_alert_on_leave,
            "default_saved_image_quality": default_saved_image_quality,
            "force_to_png_in_elliptical_crop": force_to_png_in_elliptical_crop,
            "use_cloud_image": use_cloud_image,
            "saving_pixel_ratio": saving_pixel_ratio,
            "preview_pixel_ratio": preview_pixel_ratio,
            "observe_plugin_container_size": observe_plugin_container_size,
            "show_canvas_only": show_canvas_only,
            "use_zoom_presets_menu": use_zoom_presets_menu,
            "disable_zooming": disable_zooming,
            "no_cross_origin": no_cross_origin,
            "disable_save_if_no_changes": disable_save_if_no_changes,
        }

        super().__init__(
            to=to,
            verbose_name=verbose_name,
            unique=unique,
            blank=blank,
            null=null,
            help_text=help_text,
            validators=validators,
            on_delete=on_delete,
            *args, **kwargs
        )

    def deconstruct(self) -> Any:
        name, path, args, kwargs = super().deconstruct()
        if "to" in kwargs:
            del kwargs["to"]

        kwargs["widget_kwargs"] = self.widget_kwargs
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        if "widget" in kwargs:
            del kwargs["widget"]
        
        return super().formfield(
            widget=FileRobotWidget(**self.widget_kwargs),
            **kwargs
        )




