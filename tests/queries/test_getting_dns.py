import uuid
from typing import Collection
from unittest.mock import Mock

import httpx
import inject
import pytest

from cloudflare_dns_updater.injection import InjectConfig
from cloudflare_dns_updater.queries.dns import DNSRecordsQuery
from cloudflare_dns_updater.services.dns.constants import ZoneType
from cloudflare_dns_updater.services.dns.dtos.update import UpdateDNSRecordDto
from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import (
    DNSRecords,
    DNSSingleRecord,
    ZoneID,
)
from cloudflare_dns_updater.settings import Settings

TEST_UUID = ZoneID(uuid.uuid4().hex)
TEST_DNS_RECORD = DNSSingleRecord(
    id=TEST_UUID,
    name="test.com",
    content="127.0.0.1",
    type=ZoneType.A,
    zone_id=TEST_UUID,
)


@pytest.fixture
def dns_service_mock_inject() -> None:
    class DNSServiceMock(DNSService):
        async def get_dns_records(self, zone_id: ZoneID) -> DNSRecords:
            return DNSRecords([TEST_DNS_RECORD])

        async def update_dns_records(
            self, dtos: Collection[UpdateDNSRecordDto]
        ) -> DNSRecords:
            return DNSRecords([TEST_DNS_RECORD])

    class MockInjectConfig(InjectConfig):
        @classmethod
        def dns_service(cls, settings: Settings) -> DNSService:
            return DNSServiceMock(api_token="TEST_TOKEN")

    inject.clear_and_configure(config=MockInjectConfig.bind_config)
    yield
    inject.clear_and_configure(config=InjectConfig.bind_config)


@pytest.mark.asyncio
async def test_should_get_dns_records(dns_service_mock_inject):
    # Given
    expected = [
        DNSSingleRecord(
            id=TEST_UUID,
            name="test.com",
            content="127.0.0.1",
            type=ZoneType.A,
            zone_id=TEST_UUID,
        )
    ]
    # When
    result = await DNSRecordsQuery.execute(zone_id=TEST_UUID)

    # Then
    assert result == expected
    assert isinstance(result, DNSRecords)
    assert all(isinstance(record, DNSSingleRecord) for record in result)


@pytest.mark.asyncio
async def test_should_raise_if_could_not_get_dns_records(dns_service_mock_inject):
    # Given
    dns_service = inject.instance(DNSService)
    dns_service.get_dns_records = Mock()
    dns_service.get_dns_records.side_effect = httpx.HTTPStatusError("Oops...", request=object(), response=object())  # type: ignore

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await DNSRecordsQuery.execute(zone_id=TEST_UUID)
