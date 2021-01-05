from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    LIBRARY_NAME = "cloudflare_dns_updater"
    IP_API_URL = "https://api64.ipify.org?format=json"

    @classmethod
    def disable_logging(self) -> None:
        from loguru import logger

        logger.disable(self.LIBRARY_NAME)
