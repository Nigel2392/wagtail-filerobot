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
    """
        Utility class for easily turning anything into a
        wagtail-renderable block.
        
        `{% include_block ... %}`
    """

    def get_context(self, parent_context=None):
        return {
            "self": self,
        }
    
    
    def get_template(self, context=None):
        return self.template_name
    
    
    def render_as_block(self, context=None):
        """
            Method to render the block as a wagtail block.
        """
        template = self.get_template(
            context=context,
        )

        if context is None:
            new_context = self.get_context()
        else:
            new_context = self.get_context(parent_context=dict(context))

        return _mark_safe(_render_to_string(template, new_context))


class FilerobotImageValue(BlockTemplateMixin):
    """
        Image value used to represent the underlying image instance

        This is used to make any return value from the widget
        behave like a wagtail block which can be rendered with
        `{% include_block ... %}`
    """
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
        # Initializer is the calling instance of this class.
        # It can be a django model, a wagtail block, a formfield, etc.
        self.initializer = initializer

        # The underlying image instance to use.
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
        """
            Proxy all attribute setting to the image object,
            except for the ones required by the block.
        """
        if name in self.__noproxy_fields__:
            object.__setattr__(self, name, value)
        else:
            setattr(self.image, name, value)

    @classmethod
    def from_image(cls, initializer, image: "WagtailImage") -> "Self":
        """
            Utility method to convert an image instance to a FilerobotImageValue
            Generally used in `to_python` methods and in fields.ForwardFilerobotDescriptor
        """
        if image is None:
            return None
        
        if isinstance(image, cls):
            return image
        
        if not isinstance(image, Image):
            return image
        
        return cls(initializer, image)
    

    @classmethod
    def to_pk(cls, value: "Self") -> int:
        """
            Utility method to convert a FilerobotImageValue to a pk
            Generally used in `get_prep_value` methods.
        """
        if value is None:
            return None
        
        if isinstance(value, cls):
            return value.image.pk
        
        return value

