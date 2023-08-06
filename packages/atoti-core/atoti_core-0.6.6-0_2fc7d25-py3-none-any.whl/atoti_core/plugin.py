import os
import sys
from abc import ABC
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional, Union, cast

from .base_session import BaseSessionBound
from .get_package_version import get_package_version

# https://packaging.python.org/guides/creating-and-discovering-plugins/#using-package-metadata
# The “selectable” entry points were introduced in importlib_metadata 3.6 and Python 3.10.
# Prior to those changes, entry_points accepted no parameters and always returned a dictionary of entry points
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points, version
else:
    from importlib.metadata import entry_points, version


NO_PLUGINS_FILTER = "no-plugins"

PLUGIN_FILTER_ENV_VAR = "_ATOTI_PLUGIN_FILTER"
"""Indicate which plugins to activate:
* If ``None``, all installed plugins are activated.
* If ``NO_PLUGINS_FILTER``, activate no plugins.
* Else this must be a plugin key corresponding to the only plugin to activate.
  For instance: ``"aws"``.
"""

_VERSION = get_package_version(__name__)


class Plugin(ABC):
    def activate(self) -> None:  # pylint: disable=no-self-use
        """Activate the plugin.

        It can be used to monkey patch the public API to plug the real functions.
        """
        ...

    @property
    def jar_path(self) -> Optional[Path]:
        """The path to the plugin's JAR.

        When not ``None``, the JAR will be added to the classpath of the Java process.
        """
        return None

    def init_session(  # pylint: disable=no-self-use,unused-argument
        self, session: BaseSessionBound
    ) -> None:
        """Handle newly initialized session."""
        ...


@lru_cache
def get_active_plugins(
    *, plugin_filter: Union[bool, None, str] = True
) -> Dict[str, Plugin]:
    if plugin_filter is True:
        plugin_filter = os.environ.get(PLUGIN_FILTER_ENV_VAR)
        return (
            {}
            if plugin_filter == NO_PLUGINS_FILTER
            else get_active_plugins(plugin_filter=plugin_filter)
        )
    plugins = {}
    for entry_point in entry_points(group="atoti.plugins"):
        if not plugin_filter or entry_point.name == plugin_filter:
            plugin_package_name = f"atoti-{entry_point.name}"
            plugin_version = cast(
                str,
                version(plugin_package_name),  # type: ignore[no-untyped-call]
            )
            if _VERSION != plugin_version:
                raise RuntimeError(
                    f"Cannot load plugin {plugin_package_name} v{plugin_version} because it does not have the same version as atoti-core (v{_VERSION})."
                )
            plugin_class = entry_point.load()
            plugins[entry_point.name] = plugin_class()
    return plugins
