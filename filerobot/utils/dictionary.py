class notNoneDict(dict):
    """
        Utility class to prevent not-set values to
        be passed to javascript.

        This can mess with the filerobot widget.
    """

    def __init__(self, d = None, **kwargs):
        if d is None:
            d = {}
        
        items = list(d.items())
        for key, value in items:
            if value is None:
                del d[key]

        super().__init__(d, **kwargs)
        

    def __setitem__(self, key, value):
        if value is not None:
            super().__setitem__(key, value)

