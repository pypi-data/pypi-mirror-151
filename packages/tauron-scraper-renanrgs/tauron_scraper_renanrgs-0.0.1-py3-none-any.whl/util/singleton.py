def singleton(class_):
    _instance = {}

    def get_instance(*args, **kwargs):
        if class_ not in _instance:
            _instance[class_] = class_(*args, **kwargs)
        return _instance[class_]
    return get_instance
