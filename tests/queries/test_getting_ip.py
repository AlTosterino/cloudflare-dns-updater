from unittest.mock import Mock

import httpx
import inject
import pytest

from cloudflare_dns_updater.injection import InjectConfig
from cloudflare_dns_updater.queries import DeviceIPQuery
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.services.ip.value_objects import IP


@pytest.fixture
def ip_service_mock_inject(settings, injector) -> None:
    class IPServiceMock(IPService):
        async def get_device_ip(self) -> IP:
            return IP("0.0.0.0")

    class MockInjectConfig(InjectConfig):
        @property
        def ip_service(self) -> IPService:
            return IPServiceMock()

    config = MockInjectConfig(settings=settings)
    inject.clear_and_configure(config=config.bind_config)
    yield
    config = InjectConfig(settings=settings)
    inject.clear_and_configure(config=config.bind_config)


@pytest.mark.asyncio
async def test_should_get_device_ip(ip_service_mock_inject):
    # When
    result = await DeviceIPQuery.execute()

    # Then
    assert result == "0.0.0.0"
    assert isinstance(result, IP)


@pytest.mark.asyncio
async def test_should_raise_if_could_not_get_device_ip(ip_service_mock_inject):
    # Given
    ip_service = inject.instance(IPService)
    ip_service.get_device_ip = Mock()
    ip_service.get_device_ip.side_effect = httpx.HTTPStatusError("Oops...", request=object(), response=object())  # type: ignore

    # Then
    with pytest.raises(httpx.HTTPStatusError):
        # When
        await DeviceIPQuery.execute()
