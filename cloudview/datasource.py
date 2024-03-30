from . import constants as C
from typing import Callable
import threading


class DataSource:
    def __init__(
        self,
        config: dict,
        render_fn: Callable,
        update_fn: Callable,
        update_period: int,
    ) -> None:
        self.enabled = config.get(C.KEY_ENABLED, False)
        self.config = config
        self.update_period = update_period
        self.render_fn = render_fn
        self.update_fn = update_fn

    def render(self):
        if self.enabled:
            return self.render_fn(self.config)

    def start(self):
        if self.enabled and self.config.get("cache-enabled", True):
            self.update_fn(self.config)
            self.timer = threading.Timer(self.update_period, self.start)
            self.timer.start()

    def stop(self):
        if getattr(self, "timer", None):
            self.timer.cancel()
