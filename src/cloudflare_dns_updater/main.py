import asyncio

from cloudflare_dns_updater.injection import build_inject
from cloudflare_dns_updater.use_cases import GettingDeviceIP


async def main() -> None:
    await GettingDeviceIP().execute()


if __name__ == "__main__":
    build_inject()
    asyncio.run(main())
