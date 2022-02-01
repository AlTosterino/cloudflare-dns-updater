from uuid import UUID

import attr

from cloudflare_dns_updater.services.dns.constants import ZoneType


@attr.s(frozen=True, auto_attribs=True)
class UpdateDNSRecordDto:
    content: str
    id: UUID
    name: str
    type: ZoneType
    zone_id: UUID
    ttl: int = 1
    proxied: bool = True
