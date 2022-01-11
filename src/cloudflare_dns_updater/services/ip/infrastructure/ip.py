import httpx
from loguru import logger
from services.ip.infrastructure.serializers.ip import IpifySerializer
from services.ip.interfaces.ip import IPService
from services.ip.value_objects import IP


class IpifyService(IPService):
    async def get_local_ip(self) -> IP:
        logger.debug("Getting local IP using {}", self.API_URL)
        async with httpx.AsyncClient() as client:
            result = await client.get(self.API_URL)
            result.raise_for_status()
        schema = IpifySerializer(**result.json())
        logger.debug("Got device IP: {}", schema.ip)
        return schema.ip
