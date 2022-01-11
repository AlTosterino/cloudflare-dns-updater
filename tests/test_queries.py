import httpx
import inject
import pytest
from injection import InjectConfig
from services.ip.value_objects import IP

from cloudflare_dns_updater.queries import LocalIPQuery
from cloudflare_dns_updater.settings import Settings


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_get_device_ip():
    # When
    result = await LocalIPQuery.get_device_ip()

    # Then
    assert result == "83.29.68.27"
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

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await LocalIPQuery.get_device_ip()
