from __future__ import annotations

from uuid import UUID

import attr

from cloudflare_dns_updater.services.dns.constants import ZoneType
from cloudflare_dns_updater.services.dns.value_objects import DNSSingleRecord
from cloudflare_dns_updater.services.ip.value_objects import IP


@attr.s(frozen=True, auto_attribs=True)
class UpdateDNSRecordDto:
    content: str
    id: UUID
    name: str
    type: ZoneType
    zone_id: UUID
    ttl: int = 1
    proxied: bool = True

    @classmethod
    def from_dns_single_record(
        cls, device_ip: IP, record: DNSSingleRecord
    ) -> UpdateDNSRecordDto:
        return cls(
            content=device_ip,
            id=record.id,
            name=record.name,
            type=record.type,
            zone_id=record.zone_id,
        )
