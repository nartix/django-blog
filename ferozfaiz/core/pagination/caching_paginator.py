from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.functional import cached_property


class CachingPaginator(Paginator):
    def __init__(self, object_list, per_page, cache_key, cache_timeout, orphans=0, allow_empty_first_page=True):
        self._cache_key = cache_key  # Store the custom cache key
        self._cache_timeout = cache_timeout or 30  # Store the custom cache timeout
        super().__init__(object_list, per_page, orphans=orphans,
                         allow_empty_first_page=allow_empty_first_page)

    @cached_property
    def count(self):
        count = cache.get(self._cache_key)
        if count is None:
            count = super().count
            cache.set(self._cache_key, count, self._cache_timeout)
        return count
