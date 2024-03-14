from typing import Any
from django import forms
from wagtail.images import get_image_model
from .value import FilerobotImageValue
from .widgets import FilerobotWidget



image = get_image_model()


class FilerobotField(forms.ModelChoiceField):
    
    def __init__(self, widget_kwargs = None, queryset = None, *args, **kwargs):
        if widget_kwargs is None:
            widget_kwargs = {}
        self.widget_kwargs = widget_kwargs
        
        if queryset is None:
            queryset = image.objects.all()

        if queryset.model != image:
            raise ValueError("queryset must be a queryset of image objects")

        super().__init__(queryset, *args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None
        
        return FilerobotImageValue.from_image(self, value)
        
    
    def prepare_value(self, value):
        if isinstance(value, FilerobotImageValue):
            value = value.image

        return super().prepare_value(value)


    @property   
    def widget(self):
        return FilerobotWidget(**self.widget_kwargs)
    
    @widget.setter
    def widget(self, value):
        pass


    

