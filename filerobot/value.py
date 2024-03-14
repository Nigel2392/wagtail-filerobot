from typing import Self
from django.template.loader import render_to_string as _render_to_string
from django.utils.safestring import mark_safe as _mark_safe
from wagtail.images.models import Image


class FilerobotImageValue(object):
    template_name = "filerobot/blocks/filerobot.html"

    def __init__(self, initializer, image):
        self.initializer = initializer
        self.image = image

    def __str__(self):
        return self.image.title
    
    def __bool__(self):
        return bool(self.image)
    
    def __getattr__(self, name):
        if name in [
            "image",
            "get_context",
            "get_template",
            "render_as_block",
        ]:
            return object.__getattribute__(self, name)
        
        return getattr(self.image, name)
    
    def __setattr__(self, name, value):
        if name in [
            "image",
            "initializer",
        ]:
            object.__setattr__(self, name, value)
        else:
            setattr(self.image, name, value)
    
    def get_context(self, parent_context=None):
        return {
            "self": self,
        }
    
    def get_template(self, context=None):
        return self.template_name
    
    def render_as_block(self, context=None):
        template = self.get_template(
            context=context,
        )

        if context is None:
            new_context = self.get_context()
        else:
            new_context = self.get_context(parent_context=dict(context))

        return _mark_safe(_render_to_string(template, new_context))


    @classmethod
    def from_image(cls, initializer, image) -> "Self":
        if image is None:
            return None
        
        if isinstance(image, cls):
            return image
        
        if not isinstance(image, Image):
            return image
        
        return cls(initializer, image)
    
    @classmethod
    def to_pk(cls, value: "Self") -> int:
        if value is None:
            return None
        
        if isinstance(value, cls):
            return value.image.pk
        
        return value

