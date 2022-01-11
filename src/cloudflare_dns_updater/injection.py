import inject

from cloudflare_dns_updater.services.ip.infrastructure.ip import IpifyService
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.settings import Settings


class InjectConfig:
    @classmethod
    def bind_config(cls, binder: inject.Binder) -> None:
        # ? Use __call__ instead of bind_config?
        settings_inject = cls.settings_inject()
        binder.bind(Settings, settings_inject)
        binder.bind(IPService, cls.ip_service(settings=settings_inject))

    @classmethod
    def settings_inject(cls) -> Settings:
        return Settings()

    @classmethod
    def ip_service(cls, settings: Settings) -> IPService:
        return IpifyService(api_url=settings.IP_API_URL)


def build_inject() -> None:
    inject.clear_and_configure(config=InjectConfig.bind_config)
