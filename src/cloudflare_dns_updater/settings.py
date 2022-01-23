import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    LIBRARY_NAME: str = "cloudflare_dns_updater"
    IP_API_URL: str = os.environ["IP_API_URL"]
    CLOUDFLARE_API_TOKEN: str = os.environ["CLOUDFLARE_TOKEN"]

    @classmethod
    def disable_logging(cls) -> None:
        from loguru import logger

        logger.disable(cls.LIBRARY_NAME)
