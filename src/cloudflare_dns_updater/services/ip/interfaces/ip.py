from abc import ABC as Abstract
from abc import abstractmethod
from typing import Final

from cloudflare_dns_updater.services.ip.value_objects import IP


class IPService(Abstract):
    def __init__(self, api_url: str) -> None:
        self.API_URL: Final[str] = api_url

    @abstractmethod
    async def get_local_ip(self) -> IP:
        pass
