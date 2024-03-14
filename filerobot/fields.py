from typing import Any
from django.db import models
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
)
from wagtail.images import get_image_model_string
from .value import (
    FilerobotImageValue,
)
from .widgets import (
    FilerobotWidget,
    obj,
)



class ForwardFilerobotDescriptor(ForwardManyToOneDescriptor):
    """
        Descriptor for the FilerobotField.

        This makes sure that the value behaves
        like a wagtail block when it is accessed.
    """
    def __set__(self, instance, value):
        if isinstance(value, FilerobotImageValue):
            value = value.image

        super().__set__(instance, value)

    def __get__(self, instance, owner) -> FilerobotImageValue:
        value = super().__get__(instance, owner)
        if value is None:
            return None
        
        return FilerobotImageValue.from_image(instance, value)


class FilerobotField(models.ForeignKey):
    """
        A field which automatically links to wagtail's image model.

        It uses the FilerobotWidget to render an image editor.

        The value returned when accessing this field is a FilerobotImageValue.
    """
    forward_related_accessor_class = ForwardFilerobotDescriptor

    def __init__(self,
            # Objects types for the widget.
            # These are rendered as JSON in a list
            # of django.utils.html.json_script tags.
            tabs:               list[str]             = None, # Tabs defined in constants.py
            theme:              obj.Theme             = None,
            annotations_common: obj.AnnotationsCommon = None,
            text:               obj.Text              = None,
            image:              dict                  = None,
            rect:               dict                  = None,
            ellipse:            dict                  = None,
            polygon:            dict                  = None,
            pen:                dict                  = None,
            line:               dict                  = None,
            arrow:              dict                  = None,
            watermark:          dict                  = None,
            rotate:             dict                  = None,
            crop:               dict                  = None,
            crop_preset_folder: dict                  = None,
            crop_preset_group:  dict                  = None,
            crop_preset_item:   dict                  = None,
            cloud_image:        dict                  = None,

            # Primitive types for the widget.
            # These are passed in as data-attributes
            # for the stimulus controller.
            default_tab_id:                         str  = None, # Tabs defined in constants.py
            default_tool_id:                        str  = None, # Tools defined in constants.py
            use_backend_translations:               bool = None,
            language:                               str  = None, # Inferred inside attrs by translation.get_language()
            avoid_changes_not_saved_alert_on_leave: bool = None,
            default_saved_image_quality:            int  = None,
            force_to_png_in_elliptical_crop:        bool = None,
            use_cloud_image:                        bool = None,
            saving_pixel_ratio:                     int  = None,
            preview_pixel_ratio:                    int  = None,
            observe_plugin_container_size:          bool = None,
            show_canvas_only:                       bool = None,
            use_zoom_presets_menu:                  bool = None,
            disable_zooming:                        bool = None,
            no_cross_origin:                        bool = None,
            disable_save_if_no_changes:             bool = None,

            # Help the editor with autocompletion
            # Common fields
            verbose_name = None,
            unique       = False,
            blank        = True,
            null         = True,
            help_text    = "",
            validators   = (),
            on_delete    = models.CASCADE,

            # Foreign key specific fields
            related_name       = None,
            related_query_name = None,
            limit_choices_to   = None,
            parent_link        = False,
            to_field           = None,
            db_constraint      = True,

            # utility attribute to avoid re-typing every
            # field inside of deconstruct method :^)
            widget_kwargs=None,
            
            *args, **kwargs
        ):

        # Automatically set the to field to the wagtail image model
        to = get_image_model_string()

        # Set the widget_kwargs attribute
        self.widget_kwargs = widget_kwargs or {
            # Objects
            "tabs":                                   tabs,
            "theme":                                  theme,
            "annotations_common":                     annotations_common,
            "text":                                   text,
            "image":                                  image,
            "rect":                                   rect,
            "ellipse":                                ellipse,
            "polygon":                                polygon,
            "pen":                                    pen,
            "line":                                   line,
            "arrow":                                  arrow,
            "watermark":                              watermark,
            "rotate":                                 rotate,
            "crop":                                   crop,
            "crop_preset_folder":                     crop_preset_folder,
            "crop_preset_group":                      crop_preset_group,
            "crop_preset_item":                       crop_preset_item,
            "cloud_image":                            cloud_image,
            
            # Primitive types
            "default_tab_id":                         default_tab_id,
            "default_tool_id":                        default_tool_id,
            "use_backend_translations":               use_backend_translations,
            "language":                               language,
            "avoid_changes_not_saved_alert_on_leave": avoid_changes_not_saved_alert_on_leave,
            "default_saved_image_quality":            default_saved_image_quality,
            "force_to_png_in_elliptical_crop":        force_to_png_in_elliptical_crop,
            "use_cloud_image":                        use_cloud_image,
            "saving_pixel_ratio":                     saving_pixel_ratio,
            "preview_pixel_ratio":                    preview_pixel_ratio,
            "observe_plugin_container_size":          observe_plugin_container_size,
            "show_canvas_only":                       show_canvas_only,
            "use_zoom_presets_menu":                  use_zoom_presets_menu,
            "disable_zooming":                        disable_zooming,
            "no_cross_origin":                        no_cross_origin,
            "disable_save_if_no_changes":             disable_save_if_no_changes,
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
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
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
            widget=FilerobotWidget(**self.widget_kwargs),
            **kwargs
        )




