from django import forms
from wagtail.images import get_image_model
from .widgets import FileRobotWidget



image = get_image_model()


class FileRobotField(forms.ModelChoiceField):
    
    def __init__(self, widget_kwargs = None, queryset = None, *args, **kwargs):
        if widget_kwargs is None:
            widget_kwargs = {}
        self.widget_kwargs = widget_kwargs
        
        if queryset is None:
            queryset = image.objects.all()

        if queryset.model != image:
            raise ValueError("queryset must be a queryset of image objects")

        super().__init__(queryset, *args, **kwargs)

    @property   
    def widget(self):
        return FileRobotWidget(**self.widget_kwargs)
    
    @widget.setter
    def widget(self, value):
        pass


    

