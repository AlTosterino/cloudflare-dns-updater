from uuid import UUID

import inject
import pytest

from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import (
    DNSRecords,
    DNSSingleRecord,
    ZoneID,
)


@pytest.fixture(scope="module")
def vcr_config():
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "DUMMY")],
    }


@pytest.mark.vcr()
@pytest.mark.asyncio
async def test_should_get_dns_records():
    # Given
    dns_service = inject.instance(DNSService)
    zone_id = ZoneID("457aba5ea6227a7f4d672e8845a2d5e9")

    expected = [
        DNSSingleRecord(
            id=UUID("26984dd0-6a4a-f0ac-135a-e12b4ae4bec1"), name="altosterino.com"
        ),
        DNSSingleRecord(
            id=UUID("16979338-358f-4a70-eb95-395dd3650503"),
            name="bitwarden.altosterino.com",
        ),
        DNSSingleRecord(
            id=UUID("17ba2313-616c-a4ec-9be8-3de9b934790b"),
            name="portainer.altosterino.com",
        ),
        DNSSingleRecord(
            id=UUID("760a93b0-7e59-264d-ccdc-ed8d5f535500"), name="www.altosterino.com"
        ),
    ]

    # When
    result = await dns_service.get_dns_records(zone_id=zone_id)

    # Then
    assert result == expected
    assert isinstance(result, DNSRecords)
    assert all(isinstance(record, DNSSingleRecord) for record in result)
