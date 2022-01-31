from typing import cast

import inject
from loguru import logger

from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import DNSRecords


class DNSRecordsQuery:
    DNS_SERVICE = cast(DNSService, inject.attr(DNSService))

    @classmethod
    async def execute(cls, zone_id: ZoneID) -> DNSRecords:
        logger.debug("Getting dns records using: {}", type(cls.DNS_SERVICE).__name__)
        dns_records: DNSRecords = await cls.DNS_SERVICE.get_dns_records(zone_id=zone_id)
        return dns_records
