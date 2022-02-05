from abc import ABC as Abstract
from abc import abstractmethod

from cloudflare_dns_updater.services.ip.value_objects import IP


class IPService(Abstract):
    @abstractmethod
    async def get_device_ip(self) -> IP:
        pass
