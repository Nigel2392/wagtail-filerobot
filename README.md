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
   import filerobot

   class HomePage(Page):
       content_panels = [
           FieldPanel('image', widget=FileRobotWidget(
               tabs=[
                   "Finetune",
                   "Filters",
                   "Adjust",
                   # "Watermark",
                   "Annotate",
                   # "Resize",
               ],
               # ... check init method and filerobot docs
           )),
       ]

       image = models.ForeignKey(
           "wagtailimages.Image",
       )

   ```

3. Add the URLs to your urls.py
   
      ```python
      from django.urls import path, include
   
      urlpatterns = [
         path('filerobot/', include('filerobot.urls')),
      ]
      ```