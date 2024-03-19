from django.db.models.signals import post_migrate, post_save
from django.core.cache import cache
from wagtail.models import Collection
from filerobot import (
    FILEROBOT_COLLECTION_NAME,
    FILEROBOT_COLLECTION_CACHE_KEY,
    FILEROBOT_COLLECTION_CACHE_TIMEOUT,
)


def create_filerobot_collection(sender, **kwargs):
    """
        Create the filerobot collection after manage.py migrate IF it does not exist.
        Filerobot collection should ALWAYS have a depth of 2.
        No other collection at this depth with the same name should exist.
    """
    root: Collection = Collection.objects.filter(depth=1, name=FILEROBOT_COLLECTION_NAME).first()
    if root is None:
        root = Collection.add_root(
            name=FILEROBOT_COLLECTION_NAME,
        )
    
    cache.set(
        FILEROBOT_COLLECTION_CACHE_KEY,
        root.pk,
        FILEROBOT_COLLECTION_CACHE_TIMEOUT,
    )
    

def reset_filerobot_collection_cache(sender, instance, **kwargs):
    """
        Resets the filerobot collection cache.
        See views.py for usage.
    """

    if instance.name == FILEROBOT_COLLECTION_NAME and instance.depth == 1:
        cache.delete(FILEROBOT_COLLECTION_CACHE_KEY)

    cache.set(
        FILEROBOT_COLLECTION_CACHE_KEY,
        instance.pk,
        FILEROBOT_COLLECTION_CACHE_TIMEOUT,
    )
    

post_migrate.connect(create_filerobot_collection)
post_save.connect(reset_filerobot_collection_cache, sender=Collection)
