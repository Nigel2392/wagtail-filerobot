from django.core.cache import cache
from django.http import HttpRequest
from wagtail.models import Collection
from filerobot import (
    FILEROBOT_COLLECTION_NAME,
    FILEROBOT_COLLECTION_CACHE_KEY,
    FILEROBOT_COLLECTION_CACHE_TIMEOUT,
)


def get_filerobot_collection(request: HttpRequest) -> Collection:
    """
        Retrieve the filerobot collection ID from the cache.
        This might save a query.
        See signals.py for reset logic.
    """
    if hasattr(request, "filerobot_collection") and request.filerobot_collection is not None:
        return request.filerobot_collection

    cached = cache.get(FILEROBOT_COLLECTION_CACHE_KEY)
    if cached is not None:
        collection = Collection.objects.get(pk=cached)
        
        setattr(
            request,
            "filerobot_collection",
            collection,
        )
        
        return collection

    root = Collection.get_root_nodes().filter(
        name=FILEROBOT_COLLECTION_NAME,
    )

    root = root.first()
    if root is not None:
        cache.set(
            FILEROBOT_COLLECTION_CACHE_KEY,
            root.pk,
            FILEROBOT_COLLECTION_CACHE_TIMEOUT,
        )

    setattr(
        request,
        "filerobot_collection",
        collection,
    )

    return root


def get_collection_for_request(request: HttpRequest) -> Collection:
    """
        Get the collection for the current user.

        If the collection does not exist, it will be created.

        If the user is not authenticated, a ValueError will be raised.

        The collection is created under: `FILEROBOT_COLLECTION_NAME` > `%username%`
    """
    if not request.user.is_authenticated:
        raise ValueError("User is not authenticated")
    
    collection = get_filerobot_collection(request)

    if collection is None:
        raise ValueError("No filerobot collection found")
    
    if hasattr(request, "user_collection") and request.user_collection is not None:
        return request.user_collection
    
    request.user_collection = collection
    return collection
    
    #user_collection: Collection = collection.get_children().filter(
    #    name=request.user.username,
    #).first()
#
    #if user_collection is None:
    #    user_collection = collection.add_child(
    #        name=request.user.username,
    #    )
#
    #user_collection.root_collection = collection
#
    #setattr(
    #    request,
    #    "user_collection",
    #    user_collection,
    #)
#
    #return user_collection


def get_originals_collection_for_request(request: HttpRequest):
    """
        Get the originals collection for the current user.

        If the collection does not exist, it will be created.

        If the user is not authenticated, a ValueError will be raised.

        The collection is created under: `FILEROBOT_COLLECTION_NAME` > `%username%` > `originals`
    """

    if hasattr(request, "originals_collection") and request.originals_collection is not None:
        return request.originals_collection
    
    originals = Collection.objects.filter(
        name="originals",
    ).first()

    if originals is None:
        originals = Collection.add_root(
            name="originals",
        )

    request.originals_collection = originals

    return originals

    # collection = get_collection_for_request(request)
    # originals_collection = collection.get_children().filter(
    #     name="originals",
    # ).first()
# 
    # if originals_collection is None:
    #     originals_collection = collection.add_child(
    #         name="originals",
    #     )
# 
    # originals_collection.user_collection = collection
# 
    # setattr(
    #     request,
    #     "originals_collection",
    #     originals_collection,
    # )
# 
    # return originals_collection
