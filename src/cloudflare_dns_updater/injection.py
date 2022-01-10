import inject

from cloudflare_dns_updater.settings import Settings

class InjectConfig:

    @classmethod
    def bind_config(cls, binder: inject.Binder) -> None:
        # ? Use __call__ instead of bind_config?
        binder.bind(Settings, cls.settings_inject())

    @classmethod
    def settings_inject(cls) -> Settings:
        return Settings()


def build_inject() -> None:
    inject.clear_and_configure(config=InjectConfig.bind_config)
