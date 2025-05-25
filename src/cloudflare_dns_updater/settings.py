import os
import sys
from dataclasses import dataclass, field

from loguru import logger


@dataclass(frozen=True)
class Settings:
    CLOUDFLARE_API_TOKEN: str = field(
        default_factory=lambda: os.environ.get("CLOUDFLARE_API_TOKEN")
    )
    DEBUG: bool = False

    def __post_init__(self) -> None:
        self.__set_logging()
        if self.DEBUG:
            self.__set_debug_logging()

    def __set_logging(self) -> None:
        logger.remove()
        log_format = "{time:HH:mm:ss} | {message}"
        logger.add(
            sys.stderr, format=log_format, filter="cloudflare_dns_updater", level="INFO"
        )

    def __set_debug_logging(self) -> None:
        logger.remove()
        log_format = "{level} | {time:HH:mm:ss} | {name} {message}"
        logger.add(
            sys.stderr,
            format=log_format,
            filter="cloudflare_dns_updater",
            level="DEBUG",
        )
