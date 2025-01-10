from typing import Any

from flask import current_app
from flask_caching import Cache


class RedisCache:
    @property
    def cache(
            self
    ) -> Cache:
        """
        Get Dynamically Cache Object
        """
        return current_app.cache

    def get_cache(
            self,
            cache_key: str
    ) -> Any | None:
        """
        Get Cached Value by Cache Key
        """
        cached_value: Any = self.cache.get(
            cache_key
        )

        return cached_value if cached_value else None

    def set_cache(
            self,
            cache_key: str,
            value: Any,
            timeout: int = 300
    ) -> None:
        """
        Set Cache Value by Cache Key for Some Timout
        """
        self.cache.set(
            cache_key,
            value,
            timeout=timeout
        )

    def delete_cache_value(
            self,
            cache_key: str
    ) -> None:
        """
        Delete Cached Value from Flask Cache
        """
        self.cache.delete(
            cache_key
        )
