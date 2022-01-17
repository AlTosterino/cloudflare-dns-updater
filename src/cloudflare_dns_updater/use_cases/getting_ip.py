from typing import cast

import inject
from loguru import logger

from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP

# This use case is a little bit over-engineered at first sight
# but it does hide that getting device ip requires specific service.
# User story: "Get me my device IP" is no longer coupled with anything
# and it can be called without initiating use case itself.


class GettingDeviceIP:
    IP_SERVICE = cast(IPService, inject.attr(IPService))

    @classmethod
    async def execute(cls) -> IP:
        logger.debug("Getting device IP using: {}", type(cls.IP_SERVICE).__name__)
        device_ip: IP = await cls.IP_SERVICE.get_device_ip()
        return device_ip
