from typing import List, cast

import inject
from loguru import logger

from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import DNSRecords


class DNSRecordsQuery:
    DNS_SERVICE = cast(DNSService, inject.attr(DNSService))

    @classmethod
    async def execute(cls, zone_id: ZoneID, skip: List[str]) -> DNSRecords:
        logger.info("Getting DNS Records for zone {zone_id}", zone_id=zone_id)
        logger.debug("Getting DNS records using: {}", type(cls.DNS_SERVICE).__name__)
        dns_records: DNSRecords = await cls.DNS_SERVICE.get_dns_records(
            zone_id=zone_id, skip=skip
        )
        logger.info(
            "Got {num} DNS Records for zone {zone_id}",
            num=len(dns_records),
            zone_id=zone_id,
        )
        return dns_records
