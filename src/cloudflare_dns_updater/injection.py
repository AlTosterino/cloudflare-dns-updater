from dataclasses import dataclass

import inject

from cloudflare_dns_updater.services.dns.infrastructure.dns import CloudflareService
from cloudflare_dns_updater.services.dns.interfaces.dns import DNSService
from cloudflare_dns_updater.services.ip.infrastructure.ip import IpifyService
from cloudflare_dns_updater.services.ip.interfaces.ip import IPService
from cloudflare_dns_updater.settings import Settings


@dataclass(frozen=True)
class InjectConfig:
    settings: Settings

    def bind_config(self, binder: inject.Binder) -> None:
        # ? Use __call__ instead of bind_config?
        binder.bind(Settings, self.settings)
        binder.bind(IPService, self.ip_service)
        binder.bind(DNSService, self.dns_service)

    @property
    def ip_service(self) -> IPService:
        return IpifyService()

    @property
    def dns_service(self) -> DNSService:
        return CloudflareService(api_token=self.settings.CLOUDFLARE_API_TOKEN)


def build_inject(settings: Settings) -> None:
    config = InjectConfig(settings=settings)
    inject.clear_and_configure(config=config.bind_config)
