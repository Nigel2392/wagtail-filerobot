from django.db.models.signals import post_migrate
from wagtail.models import Collection
from filerobot import FILEROBOT_COLLECTION_NAME

def create_filerobot_collection(sender, **kwargs):
    root: Collection = Collection.get_first_root_node()

    if root.get_children().filter(name=FILEROBOT_COLLECTION_NAME, depth=2).exists():
        return
    
    root.add_child(
        name=FILEROBOT_COLLECTION_NAME,
    )
    


post_migrate.connect(create_filerobot_collection)
