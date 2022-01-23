import inject
import pytest

from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.dns.value_objects import ZoneID


@pytest.mark.skip
@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_get_dns_records():
    # Given
    dns_service = inject.instance(DNSService)
    zone_id = ZoneID("457aba5ea6227a7f4d672e8845a2d5e9")

    # When
    result = await dns_service.get_dns_records(zone_id=zone_id)
