import inject
from services.ip.interfaces.ip import IPService
from services.ip.value_objects import IP


class LocalIPQuery:
    IP_SERVICE = inject.attr(IPService)

    @classmethod
    async def get_device_ip(cls) -> IP:
        return await cls.IP_SERVICE.get_local_ip()
