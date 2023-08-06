import importlib


def get_workflows_platforms():
    mod = importlib.import_module("default.github")
    if hasattr(mod, "workflows_platforms"):
        return getattr(mod, "workflows_platforms")
    mod = importlib.import_module("config.github")
    if hasattr(mod, "workflows_platforms"):
        return getattr(mod, "workflows_platforms")
    raise ValueError("cannot find worklows platformas")
