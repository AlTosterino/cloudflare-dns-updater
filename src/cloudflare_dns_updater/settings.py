import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    LIBRARY_NAME: str = "cloudflare_dns_updater"
    IP_API_URL: str = os.environ["IP_API_URL"]

    @classmethod
    def disable_logging(self) -> None:
        from loguru import logger

        logger.disable(self.LIBRARY_NAME)
