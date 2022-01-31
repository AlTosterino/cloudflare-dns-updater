from abc import ABC as Abstract
from abc import abstractmethod
from typing import Final

from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import DNSRecords


class DNSService(Abstract):
    def __init__(self, api_token: str) -> None:
        self.API_TOKEN: Final[str] = api_token

    @abstractmethod
    async def get_dns_records(self, zone_id: ZoneID) -> DNSRecords:
        pass
