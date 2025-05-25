import inject
import pytest

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.settings import Settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings(CLOUDFLARE_API_TOKEN="TEST")


@pytest.fixture(autouse=True, scope="session")
def injector(settings) -> inject.Injector:
    yield build_inject(settings=settings)
    inject.clear()
