from typing import Any

import ckan.plugins.toolkit as tk

import ckanext.gpkg_view.config as config


def gpkg_get_max_file_size() -> int:
    return config.get_max_file_size()


def gpkg_get_common_map_config() -> dict[str, Any]:
    """Get common map configuration options.

    Returns a dictionary containing all configuration options that start with
    'ckanext.spatial.common_map.' prefix. The prefix is stripped from the
    returned keys.

    Returns:
        dict[str, Any]: Map configuration options with prefix removed from keys
    """
    namespace = "ckanext.spatial.common_map."

    return {
        k.replace(namespace, ""): v
        for k, v in tk.config.items()
        if k.startswith(namespace)
    }
