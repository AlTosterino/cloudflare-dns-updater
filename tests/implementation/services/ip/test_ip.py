import httpx
import inject
import pytest

from cloudflare_dns_updater.injection import InjectConfig
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP
from cloudflare_dns_updater.settings import Settings


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


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_raise_for_status_in_get_device_ip():
    # Given
    class MockInjectConfig(InjectConfig):
        @classmethod
        def settings_inject(cls) -> Settings:
            return Settings(IP_API_URL="https://reqres.in/api/users/23")

    inject.clear_and_configure(config=MockInjectConfig.bind_config)

    ip_service = inject.instance(IPService)

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await ip_service.get_device_ip()
