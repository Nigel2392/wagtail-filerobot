from django.http import JsonResponse, HttpRequest
from django.utils.translation import gettext_lazy as _
from wagtail.models import Collection
from wagtail.images import get_image_model
from wagtail.images.forms import get_image_form
from .models import DesignState

from filerobot import FILEROBOT_COLLECTION_NAME


Image = get_image_model()
ImageForm = get_image_form(Image)

def get_collection_for_request(request: HttpRequest) -> Collection:
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    
    root: Collection = Collection.get_first_root_node()
    collection: Collection = root.get_children().filter(
        name=FILEROBOT_COLLECTION_NAME,
        depth=2,
    ).first()

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



    

# Create your views here.
def file_view(request):
    if request.method == "POST":
        collection = get_collection_for_request(request)
        POST_DATA = {
            "title": request.POST.get("title", ""),
            "collection": collection.id,
        }

        form = ImageForm(
            POST_DATA,
            request.FILES,
        )
        if not form.is_valid():
            return JsonResponse({
                "success": False,
                "errors": form.errors,
            })
        

        instance = form.save(commit=False)
        instance.uploaded_by_user = request.user

        if instance.collection != collection:
            instance.collection = collection

        instance.save()

        if "design_state" in request.POST:
            DesignState.objects.update_or_create(
                image=instance,
                defaults={"designstate": request.POST["design_state"]},
            )

        return JsonResponse({
            "success": True,
            "id": instance.id,
            "url": instance.file.url,
            "title": instance.title,
        })
        
    
    if "image_id" not in request.GET:
        return JsonResponse({
            "success": False,
            "errors": [_("No image ID specified")]
        })

    try:
        image = Image.objects.get(id=request.GET["image_id"])
    except Image.DoesNotExist:
        return JsonResponse({
            "success": False,
            "errors": [_("No image found")],
        })


    if image.uploaded_by_user and image.uploaded_by_user != request.user:
        data = {
            "success": False,
            "id": image.id,
            "url": image.file.url,
            "title": image.title,
            "editable": False,
        }

    else:
        data = {
            "success": True,
            "id": image.id,
            "url": image.file.url,
            "title": image.title,
            "editable": True,
        }

        state = DesignState.objects.filter(image=image)\
            .order_by("-updated_at")\
            .first()
        
        if state:
            data["design_state"] = state.designstate

    return JsonResponse(data)
