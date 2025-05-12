import ckan.plugins.toolkit as tk

CONF_MAX_SIZE = "ckanext.gpkg_view.max_file_size"
CONF_CACHE_DURATION = "ckanext.gpkg_view.cache_duration"
CONF_CACHE_ENABLED = "ckan.gpkg_view.cache_enabled"


def get_max_file_size() -> int:
    return tk.config[CONF_MAX_SIZE]


def get_cache_duration() -> int:
    return tk.config[CONF_CACHE_DURATION]


def get_cache_enabled() -> bool:
    return tk.config[CONF_CACHE_ENABLED]
