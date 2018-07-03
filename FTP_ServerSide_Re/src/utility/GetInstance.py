__all__ = ['get_instance']


def get_instance(module_name, class_name, *args, **kwargs):
    """
        The function 'Get Instance' returns one instance
    according to the string given

    :param module_name: name or path of the module
    :param class_name: the class to get
    :param args: the args required in the class
    :param kwargs: the kwargs required in the class
    :return: the created instance
    """
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_name, class_name)
    obj = class_meta(args, kwargs)
    return obj
