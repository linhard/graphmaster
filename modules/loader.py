import importlib
import pkgutil

from modules.registry import MODULE_REGISTRY


def load_modules():
    package = "modules"

    for _, module_name, _ in pkgutil.iter_modules(["modules"]):

        if module_name in ["registry", "loader"]:
            continue

        importlib.import_module(f"{package}.{module_name}")


def get_modules():
    return MODULE_REGISTRY
