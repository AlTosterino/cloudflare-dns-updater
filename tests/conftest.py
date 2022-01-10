import inject
import pytest

from cloudflare_dns_updater.injection import InjectConfig


@pytest.fixture(autouse=True, scope="session")
def injector() -> inject.Injector:
    yield inject.clear_and_configure(config=InjectConfig.bind_config)
    inject.clear()