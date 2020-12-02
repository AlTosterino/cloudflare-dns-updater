import httpx
from loguru import logger
from cloudflare_dns_updater.settings import Settings


def get_device_ip() -> str:
    logger.debug("Getting device IP")
    result = httpx.get(Settings.IP_API_URL)
    if result.status_code == 200:
        result_json = result.json()
        logger.debug("Got device IP: {}", result_json)
        return result_json
    return None  # TODO: Raise here
