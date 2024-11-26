import asyncio
from typing import List

from loguru import logger

from cloudflare_dns_updater.commands.dns import DNSUpdateCommand
from cloudflare_dns_updater.queries import DeviceIPQuery
from cloudflare_dns_updater.queries.dns import DNSRecordsQuery
from cloudflare_dns_updater.services.dns.dtos.update import UpdateDNSRecordDto
from cloudflare_dns_updater.services.dns.value_objects import ZoneID


async def main(skip: List[str]) -> None:
    # https://discuss.python.org/t/is-there-a-way-to-define-a-function-that-can-be-used-as-a-nomal-function-and-an-async-function/5262/5
    logger.info("Running script, skipping: {}", skip)
    zone_id = ZoneID("457aba5ea6227a7f4d672e8845a2d5e9")
    device_ip, dns_records = await asyncio.gather(
        *[
            DeviceIPQuery.execute(),
            DNSRecordsQuery.execute(zone_id=zone_id, skip=skip),
        ]
    )
    dns_records_to_update: List[UpdateDNSRecordDto] = []
    logger.info("Records to update: {}", [r.name for r in dns_records])
    for dns_record in dns_records:
        dns_records_to_update.append(
            UpdateDNSRecordDto.from_dns_single_record(
                device_ip=device_ip, record=dns_record
            )
        )
    await DNSUpdateCommand.execute(dtos=dns_records_to_update)
