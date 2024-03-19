from django.urls import reverse, path
from django.utils.functional import cached_property
from wagtail.models import Collection
from wagtail.images import get_image_model
from wagtail.images.views.chooser import (
    ImageUploadView,
    ImageChooserViewSet,
    ImageChooseView,
    ImageChooseResultsView,
)

from .utils import get_originals_collection_for_request
from .widget import (
    file_view,
)


class FileRobotImageCreateViewMixin:
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self._collection = get_originals_collection_for_request(self.request)

    def get_creation_form(self):
        form = super().get_creation_form()
        collection = getattr(self, "_collection", get_originals_collection_for_request(self.request))
        form.fields["collection"].initial = collection.pk
        form.fields["collection"].queryset = Collection.objects.filter(pk=collection.pk)
        # form.fields["collection"].widget.input_type = "hidden"
        # form.fields["collection"].widget.attrs["hidden"] = True
        return form

    def get_creation_form_kwargs(self):
        """
            Get the form kwargs.
        """
        kwargs = super().get_creation_form_kwargs()
        kwargs.setdefault("initial", {})
        kwargs["initial"].update({
            "collection": getattr(
                self, "_collection",
                get_originals_collection_for_request(self.request)
            )
        })
        return kwargs
    
    def save_form(self, form):
        """
            Save the form.
        """
        instance = form.save(commit=False)
        instance.collection = getattr(
            self, "_collection",
            get_originals_collection_for_request(self.request)
        )
        instance.save()
        return instance


class FileRobotImageChooseViewMixin(FileRobotImageCreateViewMixin):    
    @cached_property
    def collections(self):
        if self.request.user.is_superuser:
            return super().collections
        
        return Collection.objects.filter(pk__in=[
            self._collection.pk,
            self._collection.user_collection.pk,
        ])
    
    def get_object_list(self):
        return super().get_object_list().filter(collection__in=self.collections)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chosen_url_name = (
            "filerobot_chooser:select_format"
            if self.request.GET.get("select_format")
            else "filerobot_chooser:chosen"
        )

        for image in context["results"]:
            image.chosen_url = self.append_preserved_url_parameters(
                reverse(chosen_url_name, args=(image.id,))
            )

        context["collections"] = self.collections
        return context


class FileRobotImageChooseView(FileRobotImageChooseViewMixin, ImageChooseView):
    pass


class FileRobotImageChooseResultsView(FileRobotImageChooseViewMixin, ImageChooseResultsView):
    pass


class FileRobotImageUploadView(FileRobotImageCreateViewMixin, ImageUploadView):
    pass


class FileRobotImageChooserViewSet(ImageChooserViewSet):
    """
        Viewset for the filerobot image chooser.
    """
    choose_view_class = FileRobotImageChooseView
    choose_results_view_class = FileRobotImageChooseResultsView
    create_view_class = FileRobotImageUploadView

    def get_urlpatterns(self):
        return super().get_urlpatterns() + [
            path("filerobot/", file_view, name="filerobot"),
        ]


viewset = FileRobotImageChooserViewSet(
    "filerobot_chooser",
    model=get_image_model(),
    url_prefix="filerobot/chooser",
)
