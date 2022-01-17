from unittest.mock import Mock

import httpx
import inject
import pytest

from cloudflare_dns_updater.injection import InjectConfig
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP
from cloudflare_dns_updater.settings import Settings
from cloudflare_dns_updater.use_cases import GettingDeviceIP


@pytest.fixture
def ip_service_mock_inject() -> None:
    InjectConfig.bind_config

    class IPServiceMock(IPService):
        async def get_device_ip(self) -> IP:
            return IP("0.0.0.0")

    class MockInjectConfig(InjectConfig):
        @classmethod
        def ip_service(cls, settings: Settings) -> IPService:
            return IPServiceMock(api_url="")

    inject.clear_and_configure(config=MockInjectConfig.bind_config)
    yield
    inject.clear_and_configure(config=InjectConfig.bind_config)


@pytest.mark.asyncio
async def test_should_get_device_ip_from_use_case(ip_service_mock_inject):
    # When
    result = await GettingDeviceIP.execute()

    # Then
    assert result == "0.0.0.0"
    assert isinstance(result, IP)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_should_raise_if_could_not_get_device_ip(ip_service_mock_inject):
    # Given
    ip_service = inject.instance(IPService)
    ip_service.get_device_ip = Mock()
    ip_service.get_device_ip.side_effect = httpx.HTTPStatusError("Oops...", request=object(), response=object())  # type: ignore

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await GettingDeviceIP.execute()
