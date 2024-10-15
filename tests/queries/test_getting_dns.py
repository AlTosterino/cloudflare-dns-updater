import uuid
from typing import Collection, List
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

TEST_UUID = ZoneID(uuid.uuid4().hex)
TEST_DNS_RECORD = DNSSingleRecord(
    id=TEST_UUID,
    name="test.com",
    content="127.0.0.1",
    type=ZoneType.A,
    zone_id=TEST_UUID,
)


@pytest.fixture
def dns_service_mock_inject(settings) -> None:
    class DNSServiceMock(DNSService):
        async def get_dns_records(self, zone_id: ZoneID, skip: List[str]) -> DNSRecords:
            records = [TEST_DNS_RECORD]
            return DNSRecords([record for record in records if record.name not in skip])

        async def update_dns_records(
            self, dtos: Collection[UpdateDNSRecordDto]
        ) -> DNSRecords:
            return DNSRecords([TEST_DNS_RECORD])

    class MockInjectConfig(InjectConfig):
        @property
        def dns_service(self) -> DNSService:
            return DNSServiceMock(api_token="TEST_TOKEN")

    config = MockInjectConfig(settings=settings)
    inject.clear_and_configure(config=config.bind_config)
    yield
    config = InjectConfig(settings=settings)
    inject.clear_and_configure(config=config.bind_config)


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
    result = await DNSRecordsQuery.execute(zone_id=TEST_UUID, skip=[])

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
        await DNSRecordsQuery.execute(zone_id=TEST_UUID, skip=[])


@pytest.mark.asyncio
async def test_should_skip_dns_records(dns_service_mock_inject):
    # When
    result = await DNSRecordsQuery.execute(zone_id=TEST_UUID, skip=["test.com"])

    # Then
    assert not result
