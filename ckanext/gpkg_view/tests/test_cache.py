from __future__ import annotations

from datetime import datetime, timedelta, timezone

import geopandas as gpd
import pytest
from freezegun import freeze_time

import ckanext.gpkg_view.config as config
from ckanext.gpkg_view.cache import CacheManager


@pytest.mark.usefixtures("clean_file_cache")
class TestCacheManager:
    def test_hit_cache(self, geodata_frame):
        """Test caching and retrieving GeoDataFrame"""
        key = "test_key"

        assert CacheManager.get_data(key) is None

        CacheManager.set_data(key, geodata_frame.to_json())

        cached = CacheManager.get_data(key)
        assert isinstance(cached, str)
        assert cached == geodata_frame.to_json()

    def test_invalidate_cache(self, geodata_frame):
        """Test invalidating specific cache entry"""
        key = "test_key"

        CacheManager.set_data(key, geodata_frame.to_json())
        assert isinstance(CacheManager.get_data(key), str)

        CacheManager.invalidate(key)
        assert CacheManager.get_data(key) is None

    def test_invalidate_all(self, geodata_frame):
        """Test invalidating all cache entries"""
        key1, key2 = "test_key1", "test_key2"

        CacheManager.set_data(key1, geodata_frame.to_json())
        CacheManager.set_data(key2, geodata_frame.to_json())

        assert isinstance(CacheManager.get_data(key1), str)
        assert isinstance(CacheManager.get_data(key2), str)

        CacheManager.invalidate_all()

        assert CacheManager.get_data(key1) is None
        assert CacheManager.get_data(key2) is None


@pytest.mark.usefixtures("clean_file_cache")
@pytest.mark.ckan_config(config.CONF_CACHE_DURATION, 100)
class TestCacheExpiration:
    def test_cache_is_expired(self, geodata_frame):
        """Test that cache expires after configured duration"""
        key = "test_key"

        CacheManager.set_data(key, geodata_frame.to_json())

        assert isinstance(CacheManager.get_data(key), str)

        with freeze_time(datetime.now(timezone.utc) + timedelta(seconds=101)):
            assert CacheManager.get_data(key) is None

    def test_cache_is_not_expired(self, geodata_frame):
        """Test that cache remains valid before expiration"""
        key = "test_key"

        CacheManager.set_data(key, geodata_frame.to_json())
        assert isinstance(CacheManager.get_data(key), str)

        with freeze_time(datetime.now(timezone.utc) + timedelta(seconds=50)):
            cached = CacheManager.get_data(key)

            assert isinstance(cached, str)
