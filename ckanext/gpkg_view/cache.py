import os
import tempfile
import logging
import time

import ckan.plugins.toolkit as tk

from ckanext.gpkg_view.config import get_cache_duration

log = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id

    def set_data(self, data: str):
        folder_path = self.get_file_cache_path()
        file_path = os.path.join(folder_path, f"{self.resource_id}.json")

        with open(file_path, "w") as f:
            f.write(data)

    def get_data(self) -> str | None:
        file_path = os.path.join(self.get_file_cache_path(), f"{self.resource_id}.json")

        if not os.path.exists(file_path):
            return None

        if self.is_file_cache_expired(file_path):
            self.invalidate()
            return None

        with open(file_path, "r") as f:
            return f.read()

    def invalidate(self) -> None:
        file_path = os.path.join(self.get_file_cache_path(), f"{self.resource_id}.json")

        if not os.path.exists(file_path):
            return

        os.unlink(file_path)

    @staticmethod
    def get_file_cache_path() -> str:
        """Return path to the cache folder"""
        storage_path: str = tk.config["ckan.storage_path"] or tempfile.gettempdir()

        cache_path = os.path.join(storage_path, "gpkg_cache")

        os.makedirs(cache_path, exist_ok=True)

        return cache_path

    @staticmethod
    def invalidate_all() -> None:
        folder_path = CacheManager.get_file_cache_path()

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            try:
                os.unlink(file_path)
            except Exception:
                log.exception("Failed to delete file: %s", file_path)

    @staticmethod
    def remove_expired_file_cache() -> None:
        """Remove expired files from the file cache"""
        cache_path = CacheManager.get_file_cache_path()

        for filename in os.listdir(cache_path):
            file_path = os.path.join(cache_path, filename)

            if CacheManager.is_file_cache_expired(file_path):
                os.unlink(file_path)

        log.info("Expired files have been removed from the file cache")

    @staticmethod
    def is_file_cache_expired(file_path: str) -> bool:
        """Check if file cache is expired.

        Args:
            file_path: The path to the file.

        Returns:
            True if file cache is expired, otherwise False.
        """
        file_ttl = get_cache_duration()

        return time.time() - os.path.getmtime(file_path) > file_ttl
