from wagtail import blocks
from wagtail.images import get_image_model
from .forms import FileRobotField
from .widgets import FileRobotWidget



class FilerobotBlock(blocks.ChooserBlock):
    def __init__(self, widget_kwargs = None, **kwargs):
        super().__init__(**kwargs)
        self.widget_kwargs = widget_kwargs or {}
        self.target_model = get_image_model()

    @property
    def field(self):
        return FileRobotField(
            widget_kwargs=self.widget_kwargs,
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



