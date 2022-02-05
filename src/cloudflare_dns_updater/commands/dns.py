from typing import Collection, cast

import inject
from loguru import logger

from cloudflare_dns_updater.services.dns.dtos.update import UpdateDNSRecordDto
from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import DNSRecords


class DNSUpdateCommand:
    DNS_SERVICE = cast(DNSService, inject.attr(DNSService))

    @classmethod
    async def execute(cls, dtos: Collection[UpdateDNSRecordDto]) -> DNSRecords:
        logger.info("Updating {} DNS Records", len(dtos))
        logger.debug("Updating DNSRecords using: {}", type(cls.DNS_SERVICE).__name__)
        dns_records: DNSRecords = await cls.DNS_SERVICE.update_dns_records(dtos=dtos)
        logger.info("Updated {} DNS Records", len(dns_records))
        return dns_records
