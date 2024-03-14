class notNoneDict(dict):
    """
        Utility class to prevent not-set values to
        be passed to javascript.

        This can mess with the filerobot widget.
    """
    def __setitem__(self, key, value):
        if value is not None:
            super().__setitem__(key, value)

