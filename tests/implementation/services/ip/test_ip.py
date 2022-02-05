import httpx
import inject
import pytest

from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_get_device_ip():
    # Given
    ip_service = inject.instance(IPService)

    # When
    result = await ip_service.get_device_ip()

    # Then
    assert result == "217.96.155.13"
    assert isinstance(result, IP)


@pytest.mark.asyncio
async def test_should_raise_for_status_in_get_device_ip(httpx_mock):
    ip_service = inject.instance(IPService)

    # Given
    httpx_mock.add_response(status_code=400)

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await ip_service.get_device_ip()
