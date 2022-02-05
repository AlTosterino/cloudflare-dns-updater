from typing import Final

import httpx
from loguru import logger

from cloudflare_dns_updater.services.ip.infrastructure.serializers.ip import (
    IpifySerializer,
)
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP


class IpifyService(IPService):
    API_URL: Final[str] = "https://api64.ipify.org?format=json"

    async def get_device_ip(self) -> IP:
        logger.debug("Getting local IP using {}", self.API_URL)
        async with httpx.AsyncClient() as client:
            result = await client.get(self.API_URL)
            result.raise_for_status()
        result_as_json = result.json()
        logger.debug("Got response: {}", result_as_json)
        schema = IpifySerializer(**result_as_json)
        logger.debug("Got validated device IP: {}", schema.ip)
        return schema.ip
