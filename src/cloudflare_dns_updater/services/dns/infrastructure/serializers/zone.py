from typing import List
from uuid import UUID

from pydantic import BaseModel

from cloudflare_dns_updater.services.dns.value_objects.record import (
    DNSRecords,
    DNSSingleRecord,
)


class SingleRecordeSerializer(BaseModel):
    id: UUID
    name: str


class RecordsSerializer(BaseModel):
    __root__: List[SingleRecordeSerializer]

    def to_value_object(self) -> DNSRecords:
        parsed_records = [
            DNSSingleRecord(**parsed_record.dict()) for parsed_record in self.__root__
        ]
        return DNSRecords(parsed_records)
