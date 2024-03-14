from django import template
from django.template import library
from django.template.base import FilterExpression

from wagtail.images.models import Filter
from wagtail.images.utils import to_svg_safe_spec
from wagtail.images.shortcuts import (
    get_rendition_or_not_found,
)


register = library.Library()


class FilerobotImageNode(template.Node):
    """
    Node for the {% image %} tag, which resolves the image and filter spec
    expressions and then renders the image with the corresponding filter

    {% filerobot self.photo "max-320x200" as img %}
    """
    def __init__(
        self,
        image_expr,
        filter_specs,
        output_var_name=None,
        attrs={},
        preserve_svg=False,
    ):
        self.image_expr = image_expr
        self.output_var_name = output_var_name
        self.attrs = attrs
        self.filter_specs = filter_specs
        self.preserve_svg = preserve_svg

    def get_filter(self, context, preserve_svg=False):
        _filter_specs = []

        for spec in self.filter_specs:
            if isinstance(spec, FilterExpression):
                spec = spec.resolve(context)

            if isinstance(spec, str):
                _filter_specs.append(spec)

            if isinstance(spec, (list, tuple)):
                _filter_specs.extend(spec)

        if preserve_svg:
            return Filter(to_svg_safe_spec(_filter_specs))
        
        return Filter(spec="|".join(_filter_specs))

    def validate_image(self, context):
        try:
            image = self.image_expr.resolve(context)
        except template.VariableDoesNotExist:
            return

        if not image:
            if self.output_var_name:
                context[self.output_var_name] = None
            return
        
        if not hasattr(image, "get_rendition"):
            raise ValueError(
                "Image template tags expect an Image object, got %r" % image
            )

        return image

    def render(self, context):
        image = self.validate_image(context)

        if not image:
            return ""

        rendition = get_rendition_or_not_found(
            image,
            self.get_filter(
                context,
                preserve_svg=self.preserve_svg and image.is_svg()
            ),
        )

        if self.output_var_name:
            # return the rendition object in the given variable
            context[self.output_var_name] = rendition
            return ""
        else:
            # render the rendition's image tag now
            resolved_attrs = {}
            for key in self.attrs:
                resolved_attrs[key] = self.attrs[key].resolve(context)
            return rendition.img_tag(resolved_attrs)


@register.simple_tag(name="make_filter_spec")
def do_make_filter_spec(*args):
    return args


@register.tag("filerobot_image")
def do_filerobot_image(parser, token):
    """
    Image tag parser implementation. Shared between all image tags supporting filter specs
    as space-separated arguments.
    """
    tag_name, *bits = token.split_contents()
    image_expr = parser.compile_filter(bits[0])
    bits = bits[1:]

    filter_specs = []
    attrs = {}
    output_var_name = None

    as_context = False  # if True, the next bit to be read is the output variable name
    error_messages = []
    preserve_svg = False

    for bit in bits:
        if bit == "as":
            # token is of the form {% image self.photo max-320x200 as img %}
            as_context = True
        elif as_context:
            if output_var_name is None:
                output_var_name = bit
            else:
                # more than one item exists after 'as' - reject as invalid
                error_messages.append("More than one variable name after 'as'")
        elif bit == "preserve-svg":
            preserve_svg = True
        else:
            try:
                name, value = bit.split("=")
                attrs[name] = parser.compile_filter(
                    value
                )  # setup to resolve context variables as value
            except ValueError:
                filter_specs.append(
                    parser.compile_filter(bit),
                )

    if as_context and output_var_name is None:
        # context was introduced but no variable given ...
        error_messages.append("Missing a variable name after 'as'")

    if output_var_name and attrs:
        # attributes are not valid when using the 'as img' form of the tag
        error_messages.append("Do not use attributes with 'as' context assignments")

    if len(filter_specs) == 0:
        # there must always be at least one filter spec provided
        error_messages.append("Image tags must be used with at least one filter spec")

    if len(error_messages) == 0:
        return FilerobotImageNode(
            image_expr,
            filter_specs,
            attrs=attrs,
            output_var_name=output_var_name,
            preserve_svg=preserve_svg,
        )
    else:
        errors = "; ".join(error_messages)
        raise template.TemplateSyntaxError(
            f"Invalid arguments provided to {tag_name}: {errors}. "
            'Image tags should be of the form {% image self.photo max-320x200 [ custom-attr="value" ... ] %} '
            "or {% image self.photo max-320x200 as img %}. "
        )
