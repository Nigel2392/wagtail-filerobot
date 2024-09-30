from django.core.cache import cache
from django.http import HttpRequest
from wagtail.models import Collection
from filerobot import (
    FILEROBOT_COLLECTION_NAME,
    FILEROBOT_COLLECTION_CACHE_KEY,
    FILEROBOT_COLLECTION_CACHE_TIMEOUT,
)


def get_filerobot_collection() -> Collection:
    """
        Retrieve the filerobot collection ID from the cache.
        This might save a query.
        See signals.py for reset logic.
    """
    cached = cache.get(FILEROBOT_COLLECTION_CACHE_KEY)
    if cached is not None:
        return Collection.objects.get(pk=cached)
    
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
    
    collection = get_filerobot_collection()

    if collection is None:
        raise ValueError("No filerobot collection found")
    
    user_collection: Collection = collection.get_descendants().filter(
        name=request.user.username,
    ).first()

    if user_collection is None:
        user_collection = collection.add_child(
            name=request.user.username,
        )

    user_collection.root_collection = collection

    return user_collection


def get_originals_collection_for_request(request: HttpRequest):
    """
        Get the originals collection for the current user.

        If the collection does not exist, it will be created.

        If the user is not authenticated, a ValueError will be raised.

        The collection is created under: `FILEROBOT_COLLECTION_NAME` > `%username%` > `originals`
    """
    collection = get_collection_for_request(request)
    originals_collection = collection.get_descendants().filter(
        name="originals",
    ).first()

    if originals_collection is None:
        originals_collection = collection.add_child(
            name="originals",
        )

    originals_collection.user_collection = collection

    return originals_collection
