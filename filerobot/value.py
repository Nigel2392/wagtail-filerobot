from typing import Self, TYPE_CHECKING
from django.template.loader import render_to_string as _render_to_string
from django.utils.safestring import mark_safe as _mark_safe
from wagtail.images import get_image_model

if TYPE_CHECKING:
    from wagtail.images.models import (
        Image as WagtailImage,
    )


Image = get_image_model()



class BlockTemplateMixin:
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




class FilerobotImageValue(BlockTemplateMixin):
    __noproxy_fields__ = [
        "initializer",
        "image",
        "template_name",
        "get_context",
        "get_template",
        "render_as_block",
    ]

    template_name = "filerobot/blocks/filerobot.html"

    def __init__(self, initializer, image: "WagtailImage"):
        self.initializer = initializer
        self.image = image

        if not isinstance(image, Image):
            raise ValueError("image must be an instance of Image")
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.image.title})"
            
    def __str__(self):
        return str(self.image)

    def __bool__(self):
        return bool(self.image)
    
    def __getattr__(self, name):
        """
            Proxy all attribute access to the image object,
            except for the ones required by the block.
        """
        if name in self.__noproxy_fields__:
            return object.__getattribute__(self, name)
        
        return getattr(self.image, name)
    
    def __setattr__(self, name, value):
        if name in self.__noproxy_fields__:
            object.__setattr__(self, name, value)
        else:
            setattr(self.image, name, value)

    @classmethod
    def from_image(cls, initializer, image: "WagtailImage") -> "Self":
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

