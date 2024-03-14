from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images import get_image_model
from .value import FilerobotImageValue
from .forms import FileRobotField
from .widgets import FileRobotWidget
    

class FilerobotBlock(blocks.ChooserBlock):
    """
        A custom block for editing your images with filerobot image editor.

        Inherits from chooserblock for the purposes of validation.
    """
    class Meta:
        icon = "image"
        template = "filerobot/blocks/filerobot.html"
        label = _("Image Editor")


    def __init__(self, widget_kwargs = None, **kwargs):
        super().__init__(**kwargs)
        self.widget_kwargs = widget_kwargs or {}
        self.target_model = get_image_model()


    def get_queryset(self):
        return self.model_class.objects.all()


    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None
        
        return FilerobotImageValue.from_image(self, value)

    
    def get_prep_value(self, value):
        if isinstance(value, FilerobotImageValue):
            value = value.image

        return super().get_prep_value(value)


    def value_from_form(self, value):

        if isinstance(value, FilerobotImageValue):
            value = value.image

        value = super().value_from_form(value)

        if not isinstance(value, FilerobotImageValue):
            value = FilerobotImageValue.from_image(self, value)

        return value

    def value_for_form(self, value):
        if isinstance(value, FilerobotImageValue):
            value = value.image

        return super().value_for_form(value)

    @property
    def field(self):
        return FileRobotField(
            widget_kwargs=self.widget_kwargs,
            queryset=self.get_queryset(),
            required=getattr(self.meta, "required", False),
            help_text=getattr(self.meta, "help_text", None),
            validators=getattr(self.meta, "validators", ()),
        )


    @field.setter
    def field(self, value):
        pass


    @property
    def widget(self):
        return FileRobotWidget(**self.widget_kwargs)


    @widget.setter
    def widget(self, value):
        pass
