from django.db.models.signals import post_migrate
from wagtail.models import Collection
from filerobot import FILEROBOT_COLLECTION_NAME

def create_filerobot_collection(sender, **kwargs):
    if Collection.objects.filter(name=FILEROBOT_COLLECTION_NAME, depth=1).exists():
        return
    
    Collection.add_root(
        name=FILEROBOT_COLLECTION_NAME,
    )



post_migrate.connect(create_filerobot_collection)
