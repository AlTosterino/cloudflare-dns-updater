import inject
import pytest


@pytest.fixture(scope="session")
def settings() -> "Settings":
    from cloudflare_dns_updater.settings import Settings

    return Settings(CLOUDFLARE_API_TOKEN="TEST")


@pytest.fixture(autouse=True, scope="session")
def injector(settings) -> inject.Injector:
    from cloudflare_dns_updater.injection import build_inject

    yield build_inject(settings=settings)
    inject.clear()
