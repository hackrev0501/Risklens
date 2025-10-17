from __future__ import annotations

import importlib
import os
from fastapi import APIRouter

PLUGINS_DIR = os.getenv("PLUGINS_DIR", "/app/plugins")

router = APIRouter()


@router.get("/")
def list_plugins():
    base = PLUGINS_DIR
    entries = []
    if not os.path.isdir(base):
        return {"plugins": entries}
    for name in os.listdir(base):
        p = os.path.join(base, name)
        if os.path.isdir(p):
            entries.append(name)
    return {"plugins": entries}


@router.post("/run/{plugin_name}")
def run_plugin(plugin_name: str, target: str):
    mod_name = f"plugins.{plugin_name}.plugin"
    path = os.path.join(PLUGINS_DIR, plugin_name, "plugin.py")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec and spec.loader:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "run"):
            return {"result": mod.run(target)}
    return {"error": "Plugin not found or invalid"}
