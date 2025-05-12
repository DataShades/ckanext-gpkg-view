import logging

import geopandas as gpd
from flask import Blueprint
from pandas.api.types import is_datetime64_any_dtype, is_object_dtype

import ckan.lib.uploader as uploader
import ckan.plugins.toolkit as tk
from ckan import model

from ckanext.gpkg_view.cache import CacheManager
from ckanext.gpkg_view.config import get_cache_enabled, get_simplify_tolerance

log = logging.getLogger(__name__)

geopkg_preview = Blueprint("geopkg_preview", __name__)


def geopkg_fetch_geojson(package_id: str, resource_id: str) -> str:
    """
    Fetch GeoJSON from a GeoPackage file.

    Args:
        package_id: The ID of the dataset
        resource_id: The ID of the resource

    Returns:
        GeoJSON as a string
    """

    tk.check_access(
        "resource_show", {"user": tk.current_user.name}, {"id": resource_id}
    )

    resource = model.Resource.get(resource_id)

    if not resource:
        return "{}"

    cache_enabled = get_cache_enabled()

    if cache_enabled and (data := CacheManager.get_data(resource_id)):
        log.info("Returning cached geojson for resource %s", resource_id)
        return data

    if resource.url_type == "upload":
        res_uploader = uploader.get_resource_uploader({"id": resource.id})
        file_path = res_uploader.get_path(resource.id)
    else:
        file_path = resource.url

    log.info("Fetching geojson for resource %s", resource_id)

    data = extract_geojson_from_gpkg(file_path)

    if cache_enabled:
        CacheManager.set_data(resource_id, data)

    return data


def extract_geojson_from_gpkg(path: str) -> str:
    """
    Extracts GeoJSON from a GeoPackage file.

    Args:
        path: The path or URL to the GeoPackage file.

    Returns:
        GeoJSON as a string
    """

    gdf: gpd.GeoDataFrame = gpd.read_file(path)

    if simplify_tolerance := get_simplify_tolerance():
        gdf["geometry"] = gdf["geometry"].simplify(simplify_tolerance)  # type: ignore

    gdf = normalize_geodataframe_for_json(gdf)

    return gdf.to_json()


def normalize_geodataframe_for_json(df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Prepare a GeoDataFrame for JSON serialization by decoding bytes and
    formatting timestamps.

    Args:
        df: geopandas GeoDataFrame to process

    Returns:
        GeoDataFrame with bytes decoded and Timestamps serialized as strings
    """
    # Decode bytes in object columns
    object_cols = df.select_dtypes(include=["object"]).columns
    for col in object_cols:
        df[col] = df[col].apply(
            lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
        )

    # Convert all datetime-like columns to string
    for col in df.columns:
        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

        if is_object_dtype(df[col]):
            df[col] = df[col].apply(
                lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
            )

    return df


geopkg_preview.add_url_rule(
    "/dataset/<package_id>/resource/<resource_id>/geopkg-fetch-geojson",
    view_func=geopkg_fetch_geojson,
)
