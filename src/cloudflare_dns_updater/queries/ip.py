from typing import cast

import inject
from loguru import logger

from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP


class DeviceIPQuery:
    IP_SERVICE = cast(IPService, inject.attr(IPService))

    @classmethod
    async def execute(cls) -> IP:
        logger.info("Getting device IP")
        logger.debug("Getting device IP using: {}", type(cls.IP_SERVICE).__name__)
        device_ip: IP = await cls.IP_SERVICE.get_device_ip()
        logger.info("Got device IP: {}", device_ip)
        return device_ip
