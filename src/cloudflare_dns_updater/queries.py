from typing import Optional

import httpx
import inject
from loguru import logger

from cloudflare_dns_updater.settings import Settings


class DeviceQuery:
    settings = inject.attr(Settings)

    @classmethod
    async def get_device_ip(cls) -> Optional[str]:
        logger.debug("Getting device IP")
        result = httpx.get(cls.settings.IP_API_URL)
        result.raise_for_status()
        if result.status_code == 200:
            result_json = result.json()
            logger.debug("Got device IP: {}", result_json)
            device_ip: str = result_json["ip"]
            return device_ip
        return None
