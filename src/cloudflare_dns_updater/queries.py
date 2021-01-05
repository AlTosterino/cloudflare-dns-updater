from typing import Optional

import httpx
from loguru import logger

from cloudflare_dns_updater.settings import Settings


def get_device_ip() -> Optional[str]:
    logger.debug("Getting device IP")
    result = httpx.get(Settings.IP_API_URL)
    result.raise_for_status()
    if result.status_code == 200:
        result_json = result.json()
        logger.debug("Got device IP: {}", result_json)
        device_ip: str = result_json["ip"]
        return device_ip
    return None
