import asyncio
from typing import Collection, List, cast

import inject
from loguru import logger

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.queries import DeviceIPQuery
from cloudflare_dns_updater.queries.dns import DNSRecordsQuery
from cloudflare_dns_updater.services.dns.dtos.update import UpdateDNSRecordDto
from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import (
    DNSRecords,
    DNSSingleRecord,
    ZoneID,
)


# TODO: Move below to separate commands
class DNSUpdateCommand:
    DNS_SERVICE = cast(DNSService, inject.attr(DNSService))

    @classmethod
    async def execute(cls, dtos: Collection[UpdateDNSRecordDto]) -> DNSRecords:
        logger.debug("Updating DNSRecords using: {}", type(cls.DNS_SERVICE).__name__)
        dns_records: DNSRecords = await cls.DNS_SERVICE.update_dns_records(dtos=dtos)
        return dns_records


async def main() -> None:
    # https://discuss.python.org/t/is-there-a-way-to-define-a-function-that-can-be-used-as-a-nomal-function-and-an-async-function/5262/5
    zone_id = ZoneID("457aba5ea6227a7f4d672e8845a2d5e9")
    device_ip, dns_records = await asyncio.gather(
        *[DeviceIPQuery.execute(), DNSRecordsQuery.execute(zone_id=zone_id)]
    )
    dns_records_to_update: List[UpdateDNSRecordDto] = []
    for dns_record in dns_records:  # type: DNSSingleRecord
        update_dns_record_dto = UpdateDNSRecordDto(
            content=device_ip,
            id=dns_record.id,
            name=dns_record.name,
            type=dns_record.type,
            zone_id=dns_record.zone_id,
        )
        dns_records_to_update.append(update_dns_record_dto)
    await DNSUpdateCommand.execute(dtos=dns_records_to_update)


if __name__ == "__main__":
    build_inject()
    asyncio.run(main())
