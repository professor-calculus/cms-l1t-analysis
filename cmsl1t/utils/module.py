from importlib import import_module


def exists(module_name):
    try:
        import_module(module_name)
    except ImportError:
        if '.' not in module_name:
            return False
        # check if it is a member of a module instead
        tokens = module_name.split('.')
        module_name = '.'.join(tokens[:-1])
        try:
            m = import_module(module_name)
        except ImportError:
            return False
        return hasattr(m, tokens[-1])
    else:
        return True
