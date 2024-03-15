filerobot
=========

A wagtail widget to add [filerobot ](https://github.com/scaleflex/filerobot-image-editor)image editor to your wagtail fields.

Quick start
-----------

1. Add 'filerobot' to your INSTALLED_APPS setting like this:

   ```
   INSTALLED_APPS = [
   ...,
   'filerobot',
   ]
   ```
2. Import and use the widget on your model

   ```python
   from django.db import models
   from wagtail import fields
   from wagtail.models import Page
   from wagtail.admin.panels import FieldPanel

   from filerobot.widgets import FilerobotWidget
   from filerobot.blocks import FilerobotBlock as FilerobotBlock
   from filerobot.fields import FilerobotField as FilerobotImageField


   class HomePage(Page):
       image = models.ForeignKey(
           "wagtailimages.Image",
           null=True,
           blank=True,
           on_delete=models.SET_NULL,
           related_name="+",
       )

       # As an automatic foreign key field!
       filerobot_image = FilerobotImageField(
           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#tabsids
           tabs=[
               obj.TABS.FINETUNE,
               obj.TABS.FILTERS,
               obj.TABS.ADJUST,
               obj.TABS.WATERMARK,
               obj.TABS.ANNOTATE,
               obj.TABS.RESIZE,
           ],

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#annotationscommon
           annotations_common=obj.AnnotationsCommon(
               # fill:            str = None,
               # stroke:          str = None,
               # stroke_width:    int = None,
               # shadow_offset_x: int = None,
               # shadow_offset_y: int = None,
               # shadow_blur:     int = None,
               # shadow_color:    str = None,
               # shadow_opacity:  int = None,
               # opacity:         int = None,
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#Text
           text=obj.Text(
               # text:           str       = None,
               # font_family:    str       = None,
               # fonts:          list[str] = None,
               # font_size:      int       = None,
               # letter_spacing: int       = None,
               # line_height:    int       = None,
               # align:          str       = None,
               # font_style:     str       = None,
               # ...annotations_common

           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#image
           image=obj.Image(
               # fill:           str                   = None,
               # disable_upload: bool                  = False,
               # gallery:        list[obj.ImageObject] = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#rect
           rect=obj.Rect(
               # corner_radius: int = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#ellipse
           ellipse=obj.Ellipse(
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#polygon
           polygon=obj.Polygon(
               # sides: int = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#pen
           pen=obj.Pen(
               # stroke_width:                     int   = None,
               # tension:                          float = None,
               # line_cap:                         str   = None,
               # select_annotation_after_drawing:  bool  = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#line
           line=obj.Line(
               # stroke_width: int = None,
               # line_cap:     str = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#arrow
           arrow=obj.Arrow(
               # stroke_width:   int = None,
               # line_cap:       str = None,
               # pointer_length: int = None,
               # pointer_width:  int = None,
               # ...annotations_common
           ),

           # https://github.com/scaleflex/filerobot-image-editor?tab=readme-ov-file#watermark
           watermark=obj.Watermark(
               # gallery:             list[obj.WatermarkImageObject] = None,
               # text_scaling_ratio:  float                          = None,
               # image_scaling_ratio: float                          = None,
               # hide_text_watermark: bool                           = None,
           ),

           # rotate:                                 dict = None,
           # crop:                                   dict = None,
           # crop_preset_folder:                     dict = None,
           # crop_preset_group:                      dict = None,
           # crop_preset_item:                       dict = None,
           # cloud_image:                            dict = None,
         
           # default_tab_id:                         str  = None, # Tabs defined in constants.py
           # default_tool_id:                        str  = None, # Tools defined in constants.py
           # use_backend_translations:               bool = None,
           # language:                               str  = None, # Inferred inside attrs by translation.get_language()
           # avoid_changes_not_saved_alert_on_leave: bool = None,
           # default_saved_image_quality:            int  = None,
           # force_to_png_in_elliptical_crop:        bool = None,
           # use_cloud_image:                        bool = None,
           # saving_pixel_ratio:                     int  = None,
           # preview_pixel_ratio:                    int  = None,
           # observe_plugin_container_size:          bool = None,
           # show_canvas_only:                       bool = None,
           # use_zoom_presets_menu:                  bool = None,
           # disable_zooming:                        bool = None,
           # no_cross_origin:                        bool = None,
           # disable_save_if_no_changes:             bool = None,
           # typography:                             str  = None, # The font family to use across the theme.
         
           # Automatically save the image when submitting the admin form.
           # This might lag your browser for a second or 2 when saving the page.
           should_auto_save = True,
       )

       content_panels = [
           # As a widget!
           FieldPanel('image', widget=FilerobotWidget(tabs=[
               "Finetune",
               "Filters",
               "Adjust",
               "Watermark",
               "Annotate",
               "Resize",
           ])),
           FieldPanel("filerobot_image"),
           *Page.content_panels,
           FieldPanel('content'),
       ]

       content = fields.StreamField([
           # As a block!
           ('filerobot', FilerobotBlock()),
       ], blank=True, use_json_field=True)

   ```
3. Add the URLs to your urls.py

   ```python
   from django.urls import path, include

   urlpatterns = [
      path('filerobot/', include('filerobot.urls')),
   ]
   ```
