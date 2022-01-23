from abc import ABC as Abstract
from abc import abstractmethod
from typing import Final

from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import Records


class DNSService(Abstract):
    def __init__(self, api_url: str) -> None:
        self.API_URL: Final[str] = api_url

    @abstractmethod
    async def get_dns_records(self, zone_id: ZoneID) -> Records:
        pass
