from typing import List
from uuid import UUID

from pydantic import BaseModel

from cloudflare_dns_updater.services.dns.constants import ZoneType
from cloudflare_dns_updater.services.dns.value_objects import ZoneID
from cloudflare_dns_updater.services.dns.value_objects.record import (
    DNSRecords,
    DNSSingleRecord,
)


class UpdateRecordSerializer(BaseModel):
    content: str
    name: str
    proxied: bool
    ttl: int
    type: ZoneType

    class Config:
        use_enum_values = True


class SingleRecordSerializer(BaseModel):
    content: str
    id: UUID
    name: str
    type: ZoneType
    zone_id: ZoneID


class RecordsSerializer(BaseModel):
    __root__: List[SingleRecordSerializer]

    def to_value_object(self) -> DNSRecords:
        parsed_records = [
            DNSSingleRecord(**parsed_record.dict()) for parsed_record in self.__root__
        ]
        return DNSRecords(parsed_records)
