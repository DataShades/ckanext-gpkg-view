import geopandas as gpd
import pytest
from shapely.geometry import Point

from ckanext.gpkg_view.cache import CacheManager


@pytest.fixture
def clean_file_cache():
    CacheManager.invalidate_all()


@pytest.fixture
def geodata_frame():

    d = {"col1": ["name1", "name2"], "geometry": [Point(1, 2), Point(2, 1)]}
    return gpd.GeoDataFrame(d, crs="EPSG:4326")  # type: ignore
