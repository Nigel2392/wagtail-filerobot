from django.db.models.signals import post_migrate, post_save
from django.core.cache import cache
from wagtail.models import Collection
from filerobot import (
    FILEROBOT_COLLECTION_NAME,
    FILEROBOT_COLLECTION_CACHE_KEY,
    FILEROBOT_COLLECTION_CACHE_TIMEOUT,
)


def create_filerobot_collection(sender, **kwargs):
    root: Collection = Collection.get_first_root_node()

    if root.get_children().filter(name=FILEROBOT_COLLECTION_NAME, depth=2).exists():
        return
    
    root.add_child(
        name=FILEROBOT_COLLECTION_NAME,
    )
    

def reset_filerobot_collection_cache(sender, instance, **kwargs):
    if instance.name == FILEROBOT_COLLECTION_NAME and instance.depth == 2:
        cache.delete(FILEROBOT_COLLECTION_CACHE_KEY)

    cache.set(
        FILEROBOT_COLLECTION_CACHE_KEY,
        instance.pk,
        FILEROBOT_COLLECTION_CACHE_TIMEOUT,
    )
    

post_migrate.connect(create_filerobot_collection)
post_save.connect(reset_filerobot_collection_cache, sender=Collection)
