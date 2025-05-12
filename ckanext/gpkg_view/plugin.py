from typing import Any
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckan.types as types
from ckan.common import CKANConfig

from ckanext.gpkg_view.cache import CacheManager


RESOURCE_FORMATS = ["gpkg", "geopackage"]


@tk.blanket.blueprints
@tk.blanket.helpers
@tk.blanket.config_declarations
class GpkgViewPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IResourceController, inherit=True)

    # IConfigurable

    def configure(self, config: CKANConfig) -> None:
        # Remove expired file cache
        CacheManager.remove_expired_file_cache()

    # IConfigurer

    def update_config(self, config_):
        tk.add_template_directory(config_, "templates")
        tk.add_resource("assets", "gpkg_view")
        tk.add_public_directory(config_, "assets")

    # IResourceView

    def info(self):
        return {
            "name": "gpkg_view",
            "title": "GeoPackage",
            "icon": "map-location-dot",
            "iframed": True,
            "default_title": tk._("GeoPackage"),
        }

    def can_view(self, data_dict: types.DataDict) -> bool:
        return data_dict["resource"].get("format", "").lower() in RESOURCE_FORMATS

    def view_template(self, context: types.Context, data_dict: types.DataDict) -> str:
        return "geopkg_view/geopkg_preview.html"

    def setup_template_variables(self, context, data_dict):
        data_dict["resource"]["url"] = tk.url_for(
            "geopkg_preview.geopkg_fetch_geojson",
            package_id=data_dict["package"]["name"],
            resource_id=data_dict["resource"]["id"],
        )

    # IResourceController

    def before_resource_delete(
        self,
        context: types.Context,
        resource: dict[str, Any],
        resources: list[dict[str, Any]],
    ) -> None:
        CacheManager.invalidate(resource["id"])

    def after_resource_update(
        self, context: types.Context, resource: dict[str, Any]
    ) -> None:
        if resource.get("format", "").lower() in RESOURCE_FORMATS:
            CacheManager.invalidate(resource["id"])
