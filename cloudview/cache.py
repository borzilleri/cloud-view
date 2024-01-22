import time
from typing import Callable

__cache = {}


class CacheItem:
    def __init__(self, timeout: int, value_loader: Callable) -> None:
        self.timeout = timeout
        self.value_loader = value_loader
        self.update()

    def update(self):
        self.val = self.value_loader()
        self.exp = time.time() + self.timeout

    def is_expired(self):
        return time.time() > self.exp

    def get(self):
        if self.is_expired():
            self.update()
        return self.val


def get(key: str, timeout: int, loader: Callable):
    item = __cache.get(key, None)
    if not item:
        item = CacheItem(timeout, loader)
        __cache[key] = item
    return item.get()
