import ckan.plugins.toolkit as tk

CONF_MAX_SIZE = "ckanext.gpkg_view.max_file_size"
CONF_CACHE_DURATION = "ckanext.gpkg_view.cache_duration"
CONF_CACHE_ENABLED = "ckanext.gpkg_view.cache_enabled"
CONF_SIMPLIFY_TOLERANCE = "ckanext.gpkg_view.simplify_tolerance"

def get_max_file_size() -> int:
    return tk.config[CONF_MAX_SIZE]


def get_cache_duration() -> int:
    return tk.config[CONF_CACHE_DURATION]


def get_cache_enabled() -> bool:
    return tk.config[CONF_CACHE_ENABLED]


def get_simplify_tolerance() -> float:
    return tk.config[CONF_SIMPLIFY_TOLERANCE]
