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
           tabs=[
               "Finetune",
               "Filters",
               "Adjust",
               "Watermark",
               "Annotate",
               "Resize",
           ],
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
