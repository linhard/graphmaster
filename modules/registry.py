MODULE_REGISTRY = {}


def register_module(name: str, router):
    MODULE_REGISTRY[name] = router


def get_registered_modules():
    return MODULE_REGISTRY
