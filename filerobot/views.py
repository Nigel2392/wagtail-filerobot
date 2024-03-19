from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpRequest
from django.core.cache import cache

from wagtail.models import Collection
from wagtail.images import get_image_model
from wagtail.images.forms import get_image_form

from .models import DesignState

from filerobot import (
    FILEROBOT_COLLECTION_NAME,
    FILEROBOT_COLLECTION_CACHE_KEY,
    FILEROBOT_USER_MUST_MATCH as USER_MUST_MATCH,
    FILEROBOT_DISABLE_HISTORY as DISABLE_HISTORY,
)


Image = get_image_model()
ImageForm = get_image_form(Image)



def get_filerobot_collection() -> Collection:
    """
        Retrieve the filerobot collection ID from the cache.
        This might save a query.
        See signals.py for reset logic.
    """
    cached = cache.get(FILEROBOT_COLLECTION_CACHE_KEY)
    if cached is not None:
        return Collection.objects.get(pk=cached)
    
    root: Collection = Collection.get_first_root_node()
    collections = root.get_children().filter(
        name=FILEROBOT_COLLECTION_NAME,
        depth=2,
    )

    return collections.first()


def get_collection_for_request(request: HttpRequest) -> Collection:
    """
        Get the collection for the current user.

        If the collection does not exist, it will be created.

        If the user is not authenticated, a ValueError will be raised.

        The collection is created under: `FILEROBOT_COLLECTION_NAME` > `%username%`
    """
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    
    collection = get_filerobot_collection()

    if collection is None:
        raise ValueError("No filerobot collection found")
    
    user_collection: Collection = collection.get_children().filter(
        depth=3,
        path__startswith=collection.path,
        name=request.user.username,
    ).first()

    if user_collection is None:
        user_collection = collection.add_child(
            name=request.user.username,
        )

    return user_collection



def file_view(request):
    """
        File upload view to save images uploaded by the FilerobotWidget.

        Making GET requests to this view will return a JsonResponse with the image data.
        This does mean an `image_id` must be supplied in the GET request.

        Making POST requests to this view will save the image and return a JsonResponse with the image data.
        `image_id` is always supplied by the widget.
        It is up to the django setting `FILEROBOT_DISABLE_HISTORY` to determine if the image will be overridden or not.
        Very manual form handling is done.

        This view:

        - Saves the images under a collection

        - Saves image state if setting is enabled

        - Validates the user if setting is enabled

        - Will always return a JsonResponse
            - If the request is invalid, it will return a JsonResponse with success=False and 'errors' key set.
            - If the request is valid, it will return a JsonResponse with success=True and the image data.
    """

    if request.method == "POST":
        # Get proper collection for user.
        collection = get_collection_for_request(request)

        # Custom post data.
        # Images uploaded do not know the collection - the form errors.
        POST_DATA = {
            "title": request.POST.get("title", ""),
            "collection": collection.pk,
        }

        # Override old instances if history is disabled.
        # image_id get's passed by the javascript widget
        # if the instance already exists.
        instance = None
        if DISABLE_HISTORY and "image_id" in request.POST:
            try:
                instance = Image.objects.get(
                    pk=request.POST["image_id"],
                )
            except Image.DoesNotExist:
                pass
        
        # Validate ownership if the USER_MUST_MATCH setting is set.
        if (
            USER_MUST_MATCH\
            and instance\
            and instance.uploaded_by_user\
            and instance.uploaded_by_user != request.user
        ):
            return JsonResponse({
                "success": False,
                "errors": [_("You are not allowed to edit this image")],
            })
        
        # Validate form
        form = ImageForm(
            POST_DATA,
            request.FILES,
            instance=instance,
        )
        if not form.is_valid():
            return JsonResponse({
                "success": False,
                "errors": form.errors,
            })
        
        # Get an unsaved instance to possibly edit fields.
        instance = form.save(commit=False)
    
        # Set the user if it's not set.
        if not instance.uploaded_by_user:
            instance.uploaded_by_user = request.user

        # Update the collection if it's different.
        if instance.collection != collection:
            instance.collection = collection

        # Save to db.
        instance.save()

        # Save a possibly supplied design state.
        # This is so you can continue editing the image
        # where you left off.
        if not DISABLE_HISTORY and "design_state" in request.POST:
            DesignState.objects.update_or_create(
                image=instance,
                defaults={"designstate": request.POST["design_state"]},
            )

        return JsonResponse({
            "success": True,
            "id": instance.pk,
            "url": instance.file.url,
            "title": instance.title,
        })
        
    # GET only supports fetching of image data.
    # We must be supplied with the image_id.
    if "image_id" not in request.GET:
        return JsonResponse({
            "success": False,
            "errors": [_("No image ID specified")]
        })

    try:
        image = Image.objects.get(
            pk=request.GET["image_id"],
        )
    except Image.DoesNotExist:
        return JsonResponse({
            "success": False,
            "errors": [_("No image found")],
        })

    # If USER_MUST_MATCH is True, the image to edit
    # must be uploaded by the current user.
    # Otherwise a regular image tag will be shown.
    # We will not accept uploads from other users.
    if (
            USER_MUST_MATCH\
            and image.uploaded_by_user\
            and image.uploaded_by_user != request.user
            or True
        ):
        data = {
            # More info below for editable instances.
            "success": False,
            "id": image.pk,
            "url": image.file.url,
            "title": image.title,
            "editable": False,
        }

    else:
        data = {
            "success": True,

            # The image id is used to set and save the actual input field value.
            # This gets set by the widget in JS.
            "id": image.pk,

            # The widget will fetch the editable image from this url.
            "url": image.file.url,
            
            # This gets used as the default title in the widget.
            "title": image.title,

            # Indicate the full editor widget can be used.
            "editable": True,
        }

        # If history is enabled, we will fetch the latest design state.
        # The user can then continue editing the image where they left off.
        if not DISABLE_HISTORY:
            state = DesignState.objects.filter(image=image)\
                .order_by("-updated_at")\
                .first()
            
            if state:
                data["design_state"] = state.designstate

    return JsonResponse(data)
