from django.urls import path, include
from django.utils.html import json_script
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from .urls import urlpatterns

from .views.image_chooser import viewset as chooser_viewset


@hooks.register("register_admin_viewset")
def register_image_chooser_viewset():
    return chooser_viewset



@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path(
            "filerobot/",
            include((urlpatterns, "filerobot"), namespace="filerobot"),
            name="filerobot"
        )
    ]

translations = {
    "name": _('Name'),
    "save": _('Save'),
    "saveAs": _('Save as'),
    "back": _('Back'),
    "loading": _('Loading...'),
    "resetOperations": _('Reset/delete all operations'),
    "changesLoseWarningHint":
        _('If you press button “reset” your changes will lost. Would you like to continue?'),
    "discardChangesWarningHint":
        _('If you close modal, your last change will not be saved.'),
    "cancel": _('Cancel'),
    "apply": _('Apply'),
    "warning": _('Warning'),
    "confirm": _('Confirm'),
    "discardChanges": _('Discard changes'),
    "undoTitle": _('Undo last operation'),
    "redoTitle": _('Redo last operation'),
    "showImageTitle": _('Show original image'),
    "zoomInTitle": _('Zoom in'),
    "zoomOutTitle": _('Zoom out'),
    "toggleZoomMenuTitle": _('Toggle zoom menu'),
    "adjustTab": _('Adjust'),
    "finetuneTab": _('Finetune'),
    "filtersTab": _('Filters'),
    "watermarkTab": _('Watermark'),
    "annotateTabLabel": _('Annotate'),
    "resize": _('Resize'),
    "resizeTab": _('Resize'),
    "imageName": _('Image name'),
    "invalidImageError": _('Invalid image provided.'),
    "uploadImageError": _('Error while uploading the image.'),
    "areNotImages": _('are not images'),
    "isNotImage": _('is not image'),
    "toBeUploaded": _('to be uploaded'),
    "cropTool": _('Crop'),
    "original": _('Original'),
    "custom": _('Custom'),
    "square": _('Square'),
    "landscape": _('Landscape'),
    "portrait": _('Portrait'),
    "ellipse": _('Ellipse'),
    "classicTv": _('Classic TV'),
    "cinemascope": _('Cinemascope'),
    "arrowTool": _('Arrow'),
    "blurTool": _('Blur'),
    "brightnessTool": _('Brightness'),
    "contrastTool": _('Contrast'),
    "ellipseTool": _('Ellipse'),
    "unFlipX": _('Un-Flip X'),
    "flipX": _('Flip X'),
    "unFlipY": _('Un-Flip Y'),
    "flipY": _('Flip Y'),
    "hsvTool": _('HSV'),
    "hue": _('Hue'),
    "brightness": _('Brightness'),
    "saturation": _('Saturation'),
    "value": _('Value'),
    "imageTool": _('Image'),
    "importing": _('Importing...'),
    "addImage": _('+ Add image'),
    "uploadImage": _('Upload image'),
    "fromGallery": _('From gallery'),
    "lineTool": _('Line'),
    "penTool": _('Pen'),
    "polygonTool": _('Polygon'),
    "sides": _('Sides'),
    "rectangleTool": _('Rectangle'),
    "cornerRadius": _('Corner Radius'),
    "resizeWidthTitle": _('Width in pixels'),
    "resizeHeightTitle": _('Height in pixels'),
    "toggleRatioLockTitle": _('Toggle ratio lock'),
    "resetSize": _('Reset to original image size'),
    "rotateTool": _('Rotate'),
    "textTool": _('Text'),
    "textSpacings": _('Text spacings'),
    "textAlignment": _('Text alignment'),
    "fontFamily": _('Font family'),
    "size": _('Size'),
    "letterSpacing": _('Letter Spacing'),
    "lineHeight": _('Line height'),
    "warmthTool": _('Warmth'),
    "addWatermark": _('+ Add watermark'),
    "addTextWatermark": _('+ Add text watermark'),
    "addWatermarkTitle": _('Choose the watermark type'),
    "uploadWatermark": _('Upload watermark'),
    "addWatermarkAsText": _('Add as text'),
    "padding": _('Padding'),
    "paddings": _('Paddings'),
    "shadow": _('Shadow'),
    "horizontal": _('Horizontal'),
    "vertical": _('Vertical'),
    "blur": _('Blur'),
    "opacity": _('Opacity'),
    "transparency": _('Transparency'),
    "position": _('Position'),
    "stroke": _('Stroke'),
    "saveAsModalTitle": _('Save as'),
    "extension": _('Extension'),
    "format": _('Format'),
    "nameIsRequired": _('Name is required.'),
    "quality": _('Quality'),
    "imageDimensionsHoverTitle": _('Saved image size (width x height)'),
    "cropSizeLowerThanResizedWarning":
        _('Note, the selected crop area is lower than the applied resize which might cause quality decrease'),
    "actualSize": _('Actual size (100%)'),
    "fitSize": _('Fit size'),
    "addImageTitle": _('Select image to add...'),
    "mutualizedFailedToLoadImg": _('Failed to load image.'),
    "tabsMenu": _('Menu'),
    "download": _('Download'),
    "width": _('Width'),
    "height": _('Height'),
    "plus": _('+'),
    "cropItemNoEffect": _('No preview available for this crop item'),
}

@hooks.register('insert_global_admin_js')
def insert_global_admin_js():
    return json_script(translations, "filerobot-translations")
